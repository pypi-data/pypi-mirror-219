import sqlite3

import pandas as pd
import polars as pl

from ..schemas import SymbolSchema, cast, create_table_query, drop_unnecessary, write_database
from . import repository_path as rp


class RawBrandRepository:

    TABLE_NAME = "brand"

    """ダウンロードした生のCSVをデータベースに挿入するためのレポジトリ"""

    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def insert_brand_df(self, df: pl.DataFrame) -> None:
        """データベースに対象日のレコードを挿入する"""
        # 入力のチェック
        if len(df) == 0:
            raise ValueError("DataFrame is empty.")

        # レコードを一度すべて削除して再挿入
        conn = self.__get_connection()
        conn.execute("DELETE FROM brand;")
        df = preprocess_before_insert(df)
        write_database(SymbolSchema, conn, self.TABLE_NAME, df)
        conn.close()

    def drop_index(self) -> None:
        """Indexを落とす"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("DROP INDEX IF EXISTS brand_index;")
        conn.commit()
        conn.close()

    def set_index(self) -> None:
        """CodeにIndexを貼る"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute(f"CREATE INDEX IF NOT EXISTS brand_index ON {self.TABLE_NAME} (Code);")
        conn.commit()
        conn.close()

    def create_table(self) -> None:
        """新しくstockテーブルを生成する"""
        conn = self.__get_connection()
        cur = conn.cursor()
        query = create_table_query(SymbolSchema, self.TABLE_NAME)
        cur.execute(query)

        conn.commit()
        conn.close()

    def table_exists(self) -> bool:
        """brandテーブルが存在するか判定する"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='{self.TABLE_NAME}';")
        size = res.fetchone()
        is_exist: bool = size[0] > 0
        conn.commit()
        conn.close()
        return is_exist

    def records_size(self) -> int:
        """データ総数を取得"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM brand;")
        size: int = res.fetchone()[0]
        conn.commit()
        conn.close()
        return size

    def __get_connection(self) -> sqlite3.Connection:
        db_path = self.repository_path.sqlite_path
        conn = sqlite3.connect(db_path)
        return conn


def preprocess_before_insert(df: pl.DataFrame) -> pd.DataFrame:
    """Unicode型をSqliteが扱えないので予め処理する"""
    for col in df.columns:
        if df[col].dtype != pl.Utf8:
            continue
        df = df.with_columns(pl.when(pl.col(col) == "－").then(None).otherwise(pl.col(col)).alias(col))
        df = df.with_columns(pl.when(pl.col(col) == "-").then(None).otherwise(pl.col(col)).alias(col))
        df = df.with_columns(pl.when(pl.col(col) == "").then(None).otherwise(pl.col(col)).alias(col))

    df = cast(df.to_pandas(), SymbolSchema, strict=False)
    df = drop_unnecessary(df, SymbolSchema)
    return df
