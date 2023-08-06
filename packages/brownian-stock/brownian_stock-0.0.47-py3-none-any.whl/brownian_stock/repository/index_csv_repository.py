import polars as pl

from .. import const
from ..models.index_series import IndexSeries
from . import repository_path as rp


class IndexCsvRepository:

    """IndexSeriesの保存周りを管理するクラス"""

    def __init__(self, repository_path: rp.AbstractRepositoryPath) -> None:
        self.repository_path = repository_path

    def load(self, code: str) -> IndexSeries:
        """指定したコードのIndex"""
        filename = f"{code}.csv"
        df = self.repository_path.read_df(rp.DIR_COMODITY, filename)
        df = df.with_columns(pl.col(const.COL_DATE).str.strptime(pl.Date, fmt="%Y-%m-%d"))

        dates = df[const.COL_DATE].to_list()
        values = df[const.COL_INDEX_VALUE].to_list()
        index_series = IndexSeries(dates, values)
        return index_series

    def save(self, code: str, index_series: IndexSeries) -> None:
        # コモディティ用のフォルダが存在しなかったら作成する
        filename = f"{code}.csv"
        df = index_series.dataframe(as_polars=True)
        self.repository_path.save_df(rp.DIR_COMODITY, filename, df)
