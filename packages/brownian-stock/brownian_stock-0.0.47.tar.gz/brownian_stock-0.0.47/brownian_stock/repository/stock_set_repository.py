from logging import getLogger
from typing import Optional

import polars as pl
import tqdm

from ..models.stock_series import StockSeries
from ..models.stock_set import StockSet
from . import repository_path as rp

logger = getLogger(__name__)


class StockSetRepository:
    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def load(self, limit: Optional[int] = None) -> StockSet:
        stock_series_list = []
        filelist = self.repository_path.list_dir(rp.DIR_STOCK)

        if limit is not None:
            filelist = filelist[:limit]

        failed_ls = []
        for file in tqdm.tqdm(filelist):
            logger.debug(f"Loading Stock CSV `{file}`")
            try:
                if not file.name.endswith(".csv"):
                    continue
                df = self.repository_path.read_df(rp.DIR_STOCK, file)
                stock_series = StockSeries(df)
                stock_series_list.append(stock_series)
            except Exception:
                failed_ls.append(file)
        for failed_file in failed_ls:
            logger.info(f"[*] Failed to load {failed_file}")
        obj = StockSet(stock_series_list)
        return obj


def load_stock_series(csv_path: str) -> StockSeries:
    df = pl.read_csv(csv_path)
    return StockSeries(df)
