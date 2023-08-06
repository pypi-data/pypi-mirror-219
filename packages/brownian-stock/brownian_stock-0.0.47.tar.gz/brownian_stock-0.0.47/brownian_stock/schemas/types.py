from typing import Any, Type

import numpy as np
import pandas as pd
from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

AVAILABLE_TYPES = [
    str,
    int,
    float,
    bool,
    StrictStr,
    StrictInt,
    StrictFloat,
    StrictBool,
    np.datetime64,
]


class Datetime64(np.datetime64):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.is_datetime64

    @classmethod
    def is_datetime64(cls, obj: Any) -> str:
        if type(obj) != pd.Timestamp:
            raise ValueError()
        return f"datetime64: {obj}"


def cast_series(typ: Type, series: pd.Series, datetime_format: str = "%Y-%m-%d") -> pd.Series:
    if typ == str or typ == StrictStr:
        return series.astype(str)
    if typ == int or typ == StrictInt:
        return series.astype(int)
    if typ == float or typ == StrictFloat:
        return series.astype(float)
    if typ == bool or typ == StrictBool:
        return series.astype(bool)
    if typ == Datetime64:
        return pd.to_datetime(series, format=datetime_format)
    raise RuntimeError(f"Can't cast `{typ}` type.")
