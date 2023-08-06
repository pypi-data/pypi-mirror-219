from logging import getLogger
from typing import List, Optional, Tuple

import pandas as pd
import polars as pl
import sqlalchemy
import tqdm

from ..models.statements import StatementsHistory
from . import repository_path as rp

logger = getLogger(__name__)


class StatementsSQLRepository:
    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def load(self, limit: Optional[int] = None) -> List[StatementsHistory]:
        statements_list = []
        failed_list: List[Tuple[str, Exception]] = []

        conn = self.__get_connection()
        brand_df = pl.read_sql("SELECT Code FROM brand;", conn)
        brand_list = brand_df["Code"].unique().to_list()

        for brand in tqdm.tqdm(brand_list):
            try:
                df = load_statements(conn, brand)
                if df is None:
                    continue
                statements = StatementsHistory(df)
                statements_list.append(statements)
            except Exception as e:
                failed_list.append((brand, e))
        for code, error in failed_list:
            logger.error(f"[*] Failed to load {code}")
            logger.exception(error)
        return statements_list

    def __get_connection(self) -> str:
        """Sqlite用のConnectionStringを生成する
        https://sfu-db.github.io/connector-x/databases/sqlite.html
        """
        conn = "sqlite:///" + str(self.repository_path.sqlite_path.absolute())
        return conn

    def log(self, msg: str) -> None:
        print(msg)


def load_statements(conn_str: str, brand: str) -> Optional[pl.DataFrame]:
    """DBから決算情報を読み込む"""
    query = f"""
        SELECT *
        FROM statements
        JOIN brand ON statements.LocalCode = brand.Code
        WHERE statements.LocalCode = '{brand}';
    """.replace(
        "\n", ""
    )
    engine = sqlalchemy.create_engine(conn_str)
    """"""
    with engine.connect() as conn:
        pandas_df = pd.read_sql(sqlalchemy.text(query), conn)
        pandas_df.drop(columns="id", inplace=True)
        df: pl.DataFrame = pl.from_pandas(pandas_df)

    if len(df) == 0:
        return None
    return df
