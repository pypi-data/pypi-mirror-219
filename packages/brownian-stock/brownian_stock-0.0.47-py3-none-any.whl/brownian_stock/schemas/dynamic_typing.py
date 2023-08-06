import typing

import pandas as pd
from pydantic import BaseModel, ValidationError

from .types import cast_series


def cast(
    df: pd.DataFrame, model: typing.Type[BaseModel], datetime_format: str = "%Y-%m-%d", strict: bool = False
) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise ValueError()

    if strict:
        if set(df.columns) == set(model.__fields__.keys()):
            raise ValueError("dataframe is different from spefified schema.")

    for col, field in model.__fields__.items():
        # Allow lack of variable
        if col not in df.columns:
            continue
        typ = typing.cast(typing.Type, field.type_)
        df[col] = cast_series(typ, df[col], datetime_format)
    return df


def validate(df: pd.DataFrame, model: typing.Type[BaseModel]) -> bool:
    if not isinstance(df, pd.DataFrame):
        raise ValueError()

    record_ls = df.to_dict(orient="records")
    for record in record_ls:
        try:
            model.parse_obj(record)
        except ValidationError:
            return False
    return True


def drop_unnecessary(df: pd.DataFrame, model: typing.Type[BaseModel]) -> pd.DataFrame:
    columns = list(df.columns)
    definition = set(model.__fields__.keys())
    should_remove = [col for col in columns if col not in definition]
    return df.drop(columns=should_remove)
