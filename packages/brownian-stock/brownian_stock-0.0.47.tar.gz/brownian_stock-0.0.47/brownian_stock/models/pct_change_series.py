from typing import Any, List

import numpy as np
import polars as pl

from .. import const
from .abstract_series import AbstractSeries


class PctChangeSeries(AbstractSeries):

    """銘柄の前日との差分を管理するクラス"""

    AVAILABLE_KEYS = [
        const.COL_CLOSE,
        const.COL_OPEN,
        const.COL_LOW,
        const.COL_HIGH,
        const.COL_TRADING_VOLUME,
        const.COL_TURNOVER_VALUE,
    ]

    def __init__(self, stock: Any) -> None:
        base_df = stock.dataframe(as_polars=True)
        base_df = base_df.select(
            [
                pl.col(const.COL_DATE),
                pl.col(const.COL_OPEN).pct_change().fill_null(0),
                pl.col(const.COL_CLOSE).pct_change().fill_null(0),
                pl.col(const.COL_LOW).pct_change().fill_null(0),
                pl.col(const.COL_HIGH).pct_change().fill_null(0),
                pl.col(const.COL_TRADING_VOLUME).pct_change().fill_null(0),
                pl.col(const.COL_TURNOVER_VALUE).pct_change().fill_null(0),
            ]
        )

        super().__init__(base_df)
        self.stock_code = stock.stock_code
        self.company_name = stock.company_name
        self.market_type = stock.market_type
        self.sector = stock.sector
        self.sector_detail = stock.sector_detail

    def to_list(self, key: str) -> List[Any]:
        v: List[Any] = self._df[key].to_list()
        return v

    def to_array(self, key: str) -> np.ndarray[Any, Any]:
        v: np.ndarray[Any, Any] = self._df[key].to_numpy()
        return v

    def to_series(self, key: str) -> pl.Series:
        v: pl.Series = self._df[key]
        return v
