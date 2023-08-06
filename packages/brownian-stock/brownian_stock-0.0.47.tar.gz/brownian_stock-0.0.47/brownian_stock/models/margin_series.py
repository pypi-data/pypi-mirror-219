import polars as pl

from .. import const
from ..schemas import MarginInterestSchema, validate
from .abstract_series import AbstractSeries


class MarginSet:
    pass


class MarginSeries(AbstractSeries):
    def __init__(self, df: pl.DataFrame, _skip_validation: bool = False) -> None:
        # データの読み込み
        if not _skip_validation:
            if not validate(df.to_pandas(), MarginInterestSchema):
                raise ValueError("dataframe must obey to MarginInterestScheme.")

        df = df.with_columns(pl.col("Date").dt.date())
        df = df.sort(const.COL_DATE)
        super().__init__(df)
