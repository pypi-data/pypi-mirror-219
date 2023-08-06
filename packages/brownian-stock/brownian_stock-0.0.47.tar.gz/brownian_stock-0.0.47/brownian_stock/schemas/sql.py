import sqlite3
from typing import Dict, List, Type

import pandas as pd
from brownian_stock.schemas.types import Datetime64
from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr

from .dynamic_typing import validate


def create_table_query(model: Type[BaseModel], table_name: str) -> str:
    conversion_dict = {
        str: "str",
        int: "integer",
        float: "real",
        bool: "bool",
        Datetime64: "str",
        StrictStr: "str",
        StrictInt: "integer",
        StrictFloat: "real",
        StrictBool: "bool",
    }
    definition: Dict[str, str] = {}
    for key in sorted(model.__fields__.keys()):
        field = model.__fields__[key]
        sql_type = conversion_dict[field.type_]
        definition[key] = sql_type

    fields_str = ", ".join([f"'{k}' {v}" for k, v in definition.items()])
    query = f"CREATE TABLE {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, {fields_str});"
    return query


def read_sql_query(model: Type[BaseModel], table_name: str, conditions: List[str] = []) -> pd.DataFrame:
    columns = list(sorted(model.__fields__.keys()))

    columns_query = ", ".join(columns)
    where_query = " AND ".join(conditions)

    query = "SELECT {} " "FROM {}"
    query = query.format(columns_query, table_name)

    if len(conditions) > 0:
        query = query + " WHERE " + where_query
    query += ";"
    return query


def write_database(model: Type[BaseModel], connection: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    if not validate(df, model):
        raise RuntimeError("Validation Failed.")
    for col, field in model.__fields__.items():
        if field.type_ == Datetime64:
            df[col] = df[col].dt.strftime("%Y-%m-%d")
    df.to_sql(table_name, connection, if_exists="append", index=False)
