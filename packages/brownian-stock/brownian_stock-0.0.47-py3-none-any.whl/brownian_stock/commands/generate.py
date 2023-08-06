import argparse
import datetime
import logging
import os
from dataclasses import dataclass
from typing import Optional

import dacite
import humanize
import polars as pl
from brownian_stock.repository import (
    AbstractRepositoryPath,
    RawBrandRepository,
    RawMarginInterestRepository,
    RawStatementsRepository,
    RawStockRepository,
    RepositoryPath,
    S3RepositoryPath,
    StatementsCSVRepository,
    StatementsSQLRepository,
    StockCSVRepository,
    StockSQLRepository,
)
from brownian_stock.repository import repository_path as rp

from .. import const

TABLE_PRICES = "prices"
TABLE_STATEMENTS = "statements"


@dataclass
class GenerateArgs:
    generate_csv: bool
    dir_path: Optional[str]
    s3_bucket: Optional[str]
    db_connection: Optional[str]
    limit: Optional[int]

    def validate(self) -> None:
        if (self.dir_path is not None) and (self.s3_bucket is not None):
            raise ValueError("You must specify either of `dir_path` or `s3_bucket`")


def run_generate(raw_args: argparse.Namespace) -> None:
    logger = logging.getLogger(__name__)
    args_dict = vars(raw_args)
    args = dacite.from_dict(GenerateArgs, args_dict)
    args.validate()

    repository_path: AbstractRepositoryPath

    if args.s3_bucket:
        if args.db_connection is None:
            raise ValueError("`db_connection` must be specified when use `--s3_bucket` option")
        repository_path = S3RepositoryPath(args.s3_bucket, args.db_connection)
    elif args.dir_path:
        dir_path = os.path.expanduser(args.dir_path)
        repository_path = RepositoryPath(dir_path, db_connection=args.db_connection)
    else:
        dir_path = const.DEFAULT_REPOSITORY_DIR
        repository_path = RepositoryPath(dir_path, db_connection=args.db_connection)

    insert_brand_csv(repository_path, logger)
    insert_stock_csv(repository_path, logger, args.limit)
    insert_statements_csv(repository_path, logger, args.limit)
    insert_margin_interest_csv(repository_path, logger, args.limit)

    if args.generate_csv:
        create_statements_csv(repository_path, logger)
        create_stock_csv(repository_path, logger)


def insert_stock_csv(
    repository_path: AbstractRepositoryPath, logger: logging.Logger, limit: Optional[int] = None
) -> None:
    """保存した株価のCSVをDBに挿入していく"""
    logger.info("[*] Start stock csv insertion.")
    stock_repo = RawStockRepository(repository_path)
    if not stock_repo.table_exists():
        stock_repo.create_table()

    try:
        stock_repo.drop_index()
        logger.info("Drop the index on stock table.")
    except Exception as e:
        logger.info("Failed to drop the index on stock table.")
        logger.exception(e)

    existing_date = stock_repo.existing_date()

    file_list = list(sorted(repository_path.list_dir(rp.DIR_RAW_STOCK)))
    if limit is not None:
        limit_size = min(len(file_list), limit)
        file_list = file_list[:limit_size]
    size_str = humanize.intcomma(len(file_list))
    logger.info(f"The planned size of the raw_stock CSV to be inserted is {size_str}")
    for csv_path in file_list:
        # ファイル名から日付を読み込む
        date_str = csv_path.replace(".csv", "")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            logger.error(f"Failed to parse date from filename. Filename is {csv_path}.")
            continue

        if date in existing_date:
            logger.debug(f"Records already exists. Skip insert {csv_path}.")
            continue

        df = repository_path.read_df(rp.DIR_RAW_STOCK, csv_path)
        if df is None:
            logger.debug(f"DataFrame for {date_str} is empty. Skip insertion.")
            continue
        df = df.with_columns(pl.col("Date").str.strptime(pl.Date, fmt="%Y-%m-%d"))

        try:
            stock_repo.insert_daily_df(df)
            logger.info(f"Success to insert {csv_path}.")
        except Exception as e:
            logger.error(f"Error occurred until inserting {csv_path}.")
            logger.exception(e)

    try:
        stock_repo.set_index()
        logger.info("Set the index on stock table.")
    except Exception as e:
        logger.error("Failed to set the index on stock table.")
        logger.exception(e)

    size_str = humanize.intcomma(stock_repo.records_size())
    logger.info(f"Total record size of `stock` table is {size_str}.")
    logger.info("[*] Complete to insert stock CSV.")


def insert_statements_csv(
    repository_path: AbstractRepositoryPath, logger: logging.Logger, limit: Optional[int] = None
) -> None:
    statements_repo = RawStatementsRepository(repository_path)
    if not statements_repo.table_exists():
        statements_repo.create_table()

    logger.info("[*] Start statements csv insertion.")
    try:
        statements_repo.drop_index()
        logger.info("Drop the index on statements table.")
    except Exception as e:
        logger.info("Failed to drop the index on statements table.")
        logger.exception(e)

    existing_date = statements_repo.existing_date()
    file_list = list(sorted(repository_path.list_dir(rp.DIR_RAW_STATEMENTS)))
    if limit is not None:
        limit_size = min(len(file_list), limit)
        file_list = file_list[:limit_size]

    size_str = humanize.intcomma(len(file_list))
    logger.info(f"The planned size of the raw_statements CSV to be inserted is {size_str}.")
    for csv_path in file_list:
        # ファイル名から日付を読み込む
        date_str = csv_path.replace(".csv", "")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            logger.error(f"Failed to parse date from filename. Filename is {csv_path}.")
            continue

        # 既に存在していた場合には処理をスキップ
        if date in existing_date:
            logger.debug(f"Records already exists. Skip insert {csv_path}.")
            continue

        df = repository_path.read_df(rp.DIR_RAW_STATEMENTS, csv_path)
        if df is None:
            continue
        df = df.with_columns(pl.col("DisclosedDate").str.strptime(pl.Date, fmt="%Y-%m-%d"))

        try:
            statements_repo.insert_statements_df(df)
            logger.info(f"Success to insert {csv_path}.")
        except Exception as e:
            logger.error(f"Error occurred until inserting {csv_path}.")
            logger.exception(e)

    try:
        statements_repo.set_index()
        logger.info("Set the index on statements table.")
    except Exception as e:
        logger.info("Failed setting the index on statements table.")
        logger.exception(e)

    size_str = humanize.intcomma(statements_repo.records_size())
    logger.info(f"Total record size of `statements` table is {size_str}.")
    logger.info("[*] Complete to insert `statements` csv.")


def insert_brand_csv(repository_path: AbstractRepositoryPath, logger: logging.Logger) -> None:
    """ダウンロードした銘柄一覧をデータベースに格納する"""
    logger.info("[*] Start brand CSV insertion.")
    brand_repo = RawBrandRepository(repository_path)
    if not brand_repo.table_exists():
        brand_repo.create_table()

    df = repository_path.read_df(rp.DIR_BRAND, "brand.csv")
    if df is None:
        raise RuntimeError("Failed to load brand dataframe.")
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, fmt="%Y-%m-%d"))
    brand_repo.insert_brand_df(df)

    size = brand_repo.records_size()
    logger.info(f"Total record size of `brand` table is {size}")
    logger.info("[*] Complete to insert brand CSV.")


def insert_margin_interest_csv(
    repository_path: AbstractRepositoryPath, logger: logging.Logger, limit: Optional[int] = None
) -> None:
    """信用取引残高の情報をDBに格納する"""
    logger.info("[*] Start margin_interest CSV insertion.")
    margin_repo = RawMarginInterestRepository(repository_path)

    if not margin_repo.table_exists():
        margin_repo.create_table()

    try:
        margin_repo.drop_index()
        logger.info("Drop the index on margin_interest table.")
    except Exception as e:
        logger.info("Failed to drop the index on margin_interest table.")
        logger.exception(e)

    existing_date = margin_repo.existing_date()
    file_list = list(sorted(repository_path.list_dir(rp.DIR_RAW_MARGIN_INTEREST)))
    if limit is not None:
        limit_size = min(len(file_list), limit)
        file_list = file_list[:limit_size]

    size_str = humanize.intcomma(len(file_list))
    logger.info(f"The planned size of the raw margin_interest CSV to be inserted is {size_str}.")
    for csv_path in file_list:
        # ファイル名から日付を読み込む
        date_str = csv_path.replace(".csv", "")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            logger.error(f"Failed to parse date from filename. Filename is {csv_path}.")
            continue

        # 既に存在していた場合には処理をスキップ
        if date in existing_date:
            logger.debug(f"Records already exists. Skip insert {csv_path}.")
            continue

        df = repository_path.read_df(rp.DIR_RAW_MARGIN_INTEREST, csv_path)
        if df is None:
            continue
        df = df.with_columns(pl.col("Date").str.strptime(pl.Date, fmt="%Y-%m-%d"))

        try:
            margin_repo.insert_df(df)
            logger.info(f"Success to insert {csv_path}.")
        except Exception as e:
            logger.error(f"Error occurred until inserting {csv_path}.")
            logger.exception(e)

    try:
        margin_repo.set_index()
        logger.info("Set the index on margin_interest table.")
    except Exception as e:
        logger.info("Failed setting the index on margin_interest table.")
        logger.exception(e)


def create_stock_csv(repository_path: AbstractRepositoryPath, logger: logging.Logger) -> None:
    """Databaseに格納した情報を集計して個別銘柄のCSVとして吐き出す"""
    logger.info("Loading stock set from sqlite database.")
    sql_repo = StockSQLRepository(repository_path)
    logger.info("Generating stock csv.")
    csv_repo = StockCSVRepository(repository_path)
    stock_set = sql_repo.load()
    csv_repo.save(stock_set)


def create_statements_csv(repository_path: AbstractRepositoryPath, logger: logging.Logger) -> None:
    """Databaseに格納した情報を集計して個別銘柄のCSVとして吐き出す"""
    # レポジトリの初期化
    logger.info("Loading stock set from sqlite database.")
    sql_repo = StatementsSQLRepository(repository_path)
    logger.info("Generating statements csv.")
    csv_repo = StatementsCSVRepository(repository_path)

    # 処理の実行
    stock_set = sql_repo.load()
    csv_repo.save(stock_set)
