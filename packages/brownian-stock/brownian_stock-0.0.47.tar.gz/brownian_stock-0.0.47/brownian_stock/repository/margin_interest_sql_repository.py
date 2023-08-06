import re
import typing
from logging import getLogger
from typing import Dict, List, Optional, Tuple

import pandas as pd
import polars as pl
import tqdm
from sqlalchemy import create_engine, text

from ..models.margin_series import MarginSeries
from ..schemas import MarginInterestSchema, cast, read_sql_query, validate
from . import BrandRepository
from . import repository_path as rp

logger = getLogger(__name__)


class MarginInterestSQLRepository:
    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def load(self, limit: Optional[int] = None) -> Dict[str, MarginSeries]:
        margin_interest_dict: Dict[str, MarginSeries] = {}
        failed_list: List[Tuple[str, Exception]] = []

        conn = self.repository_path.connection_str
        symbols = self.symbol_list()

        if limit is not None:
            symbols = symbols[:limit]

        for symbol in tqdm.tqdm(symbols):
            try:
                df = load_margin_interest(conn, symbol)
                series = MarginSeries(df, _skip_validation=False)
                margin_interest_dict[typing.cast(str, symbol)] = series
            except Exception as e:
                failed_list.append((symbol, e))
        for code, error in failed_list:
            logger.error(f"[*] Failed to load {code}")
            logger.exception(error)
        return margin_interest_dict

    def symbol_list(self) -> List[str]:
        symbol_repo = BrandRepository(self.repository_path)
        symbols = symbol_repo.load()
        return [s.code for s in symbols]


def load_margin_interest(conn_str: str, brand: str) -> pl.DataFrame:
    engine = create_engine(conn_str)
    query = read_sql_query(MarginInterestSchema, "margin_interest", [f"Code == {brand}"])
    df = pd.read_sql_query(text(query), engine)
    df = cast(df, MarginInterestSchema)
    if not validate(df, MarginInterestSchema):
        raise IOError("Failed to cast dataframe to MarginInterestSchema")
    if len(df) == 0:
        raise IOError(f"Tried to extract stock price information for the {brand}, but there were no results.")
    pldf = pl.from_pandas(df)
    return pldf


def is_code(code_str: str) -> bool:
    ok = re.match(r"^\d\d\d\d\d$", code_str)
    return ok is not None
