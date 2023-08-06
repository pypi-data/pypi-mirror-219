import abc
import logging
from typing import Any, Dict, Type, Union

import pandas as pd
import polars as pl
from pydantic import BaseModel, StrictStr, ValidationError
from sqlalchemy import Column, MetaData, Table

logger = logging.getLogger(__name__)


class Converter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def polars_expr(self, name: str) -> pl.Expr:
        pass


class StrictStrConverter(Converter):
    def polars_expr(self, name: str) -> pl.Expr:
        return pl.col(name).cast(pl.Utf8)


class StrConverter(Converter):
    def polars_expr(self, name: str) -> pl.Expr:
        return pl.col(name).cast(pl.Utf8)


class FloatConverter(Converter):
    def polars_expr(self, name: str) -> pl.Expr:
        return pl.col(name).cast(pl.Float64)


class BooleanConverter(Converter):
    def polars_expr(self, name: str) -> pl.expr:

        expr = (
            pl.when(pl.col(name).is_null())
            .then(None)
            .otherwise(pl.col(name).cast(pl.Utf8).str.to_lowercase() == "true")
            .alias(name)
        )
        return expr


CONVERSION_MAP: Dict[str, Type[Converter]] = {
    "StrictStr": StrictStrConverter,
    "string": StrictStrConverter,
    "number": FloatConverter,
    "boolean": BooleanConverter,
}


class Property(BaseModel):
    title: str
    type: str


class Schema(BaseModel):
    properties: Dict[str, Property]


def cast_with_model(df: pl.DataFrame, model: Type[BaseModel], strict: bool = True) -> pl.DataFrame:
    """Cast dataframe based on the model.

    Args:
        df(pl.DataFrame)
    """

    schema = Schema.parse_obj(model.schema())
    properties = schema.properties
    for name, property in properties.items():
        type_name = property.type
        try:
            converter_class = CONVERSION_MAP[type_name]
            converter = converter_class()
        except KeyError:
            message = f"Unknown type {type_name} has specified for column {name}"

        if name not in df.columns:
            message = f"DataFrame doesn't have `{name}` column."
            if strict and (name not in df.columns):
                raise KeyError(message)
            else:
                logger.warning(message)
                continue

        try:
            df = df.with_columns(converter.polars_expr(name))

        except Exception:
            print(df[name])
            raise RuntimeError(f"conversion to {type_name} failed when processing column '{name}'")
    return df


def log_validation_details(idx: Any, d: dict, ex: ValidationError, limit: int = 100) -> None:
    # https://github.com/pydantic/pydantic/issues/784
    values = {}
    for error in ex.errors():
        loc = error["loc"]
        value = d
        for field in loc:
            if field == "__root__":
                break
            value = value[field]
        values[".".join([str(location) for location in loc])] = value

    idx = str(idx)[:limit]
    for k, v in values.items():
        k = str(k)[:limit]
        v = str(v)[:limit]
        logger.error(f"Validation Error @{idx} {k}: {v}")


def validate_dataframe(df: Union[pd.DataFrame, pl.DataFrame], model: Type[BaseModel]) -> bool:
    if isinstance(df, pl.DataFrame):
        df = df.to_pandas()

    record_ls = df.to_dict(orient="records")
    index = df.index
    ok = True
    for idx, record in zip(index, record_ls):
        try:
            model.parse_obj(record)
        except ValidationError as e:
            raise e
            # log_validation_details(idx, record, e)
    return ok


def create_model_table_query(model: Type[BaseModel], table_name: str) -> str:
    conversion_dict = {
        StrictStr: "str",
        str: "str",
        float: "real",
        int: "integer",
    }
    definition: Dict[str, str] = {}
    for key, field in model.__fields__.items():
        sql_type = conversion_dict[field.type_]
        definition[key] = sql_type

    fields_str = ",".join([f"'{k}' {v}" for k, v in definition.items()])
    query = f"""
        CREATE TABLE {table_name}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {fields_str}
    );"""
    return query
