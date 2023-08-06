import argparse
import datetime
import io
import logging
import os
import time
import warnings
from dataclasses import dataclass
from typing import List, Optional

import dacite
from dateutil.relativedelta import relativedelta

from ..models.calendar import Calendar
from ..repository import AbstractRepositoryPath, IndexCsvRepository, RepositoryPath, S3RepositoryPath
from ..repository import repository_path as rp
from ..services import jquants, yahoo
from ..services.dot_file import load_config

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DownloadArgs:
    only_stock: bool
    only_brand: bool
    only_statements: bool
    only_margin_interests: bool
    only_yahoo: bool

    # Repository Settings
    dir_path: Optional[str]
    s3_bucket: Optional[str]
    db_connection: Optional[str]

    limit: Optional[int]
    force: bool
    interval: int

    dot_path: Optional[str]
    username: Optional[str]
    password: Optional[str]

    def validate(self) -> None:
        if self.flag_list.count(True) > 1:
            raise ValueError("Can't use multpile only flags.")

        # 認証情報関連のバリデーション
        if not (self.dot_path is None or self.username is None):
            raise ValueError("Either `dot_path` or `username` can use.")

        if not (self.dot_path is None or self.password is None):
            raise ValueError("Either `dot_path` or `password` can use.")

        # データ保存先のバリデーション
        if (self.s3_bucket is not None) and (self.dir_path is not None):
            raise ValueError("You must specify either `dir_path` or `s3_bucket`")

    @property
    def flag_list(self) -> List[bool]:
        return [self.only_stock, self.only_brand, self.only_statements, self.only_yahoo, self.only_margin_interests]

    @property
    def do_brand(self) -> bool:
        if self.flag_list.count(True) == 0:
            return True
        if self.only_brand:
            return True
        return False

    @property
    def do_stock(self) -> bool:
        if self.flag_list.count(True) == 0:
            return True
        if self.only_stock:
            return True
        return False

    @property
    def do_statements(self) -> bool:
        if self.flag_list.count(True) == 0:
            return True
        if self.only_statements:
            return True
        return False

    @property
    def do_yahoo(self) -> bool:
        if self.flag_list.count(True) == 0:
            return True
        if self.only_yahoo:
            return True
        return False

    @property
    def do_margin_interests(self) -> bool:
        if self.flag_list.count(True) == 0:
            return True
        if self.only_margin_interests:
            return True
        return False

    @property
    def repository_path(self) -> AbstractRepositoryPath:
        db_connection = self.db_connection
        if self.s3_bucket:
            if db_connection is None:
                db_connection = "./db.sqlite"
            return S3RepositoryPath(self.s3_bucket, db_connection)
        elif self.dir_path:
            return RepositoryPath(self.dir_path)
        else:
            os.makedirs("jquants", exist_ok=True)
            return RepositoryPath("./jquants")


def run_download(raw_args: argparse.Namespace) -> None:
    args_dict = vars(raw_args)
    args = dacite.from_dict(DownloadArgs, args_dict)
    args.validate()

    username = args.username
    password = args.password

    """設定ファイルからユーザー情報を読み込み"""
    config = load_config(args.dot_path)
    if config is not None:
        if username is None:
            username = config.username
        if password is None:
            password = config.password
    if username is None or password is None:
        raise RuntimeError("Can not read user id from dot file..")

    auth = jquants.JquantsAuthToken(username, password)
    auth.login()
    repository_path = args.repository_path

    if args.do_brand:
        # ブランド一覧を取得
        brand_crawler = BrandCrawler(repository_path, auth)
        brand_crawler.crawl()

    if args.do_stock:
        # 株価情報を更新
        stock_crawler = DailyStockCrawler(repository_path, auth)
        stock_crawler.crawl(limit=args.limit, interval=args.interval, force=args.force)
        auth.refresh()

    if args.do_statements:
        # 決算情報の更新
        statements_crawler = DailyStatementsCrawler(repository_path, auth)
        statements_crawler.crawl(limit=args.limit, interval=args.interval, force=args.force)
        auth.refresh()

    if args.do_margin_interests:
        # 信用取引関連情報の更新
        margin_crawler = MarginInterestCrawler(repository_path, auth)
        margin_crawler.crawl(limit=args.limit, interval=args.interval, force=args.force)
        auth.refresh()

    if args.do_yahoo:
        # yahooから指数の情報を取得
        yahoo_crawler = YahooIndexCrawler(repository_path)
        yahoo_crawler.crawl()


class DailyStockCrawler:
    def __init__(
        self,
        repository_path: AbstractRepositoryPath,
        auth: jquants.JquantsAuthToken,
        logger: Optional[logging.Logger] = None,
        crawl_start: Optional[datetime.date] = None,
        crawl_end: Optional[datetime.date] = None,
    ) -> None:
        self.repository_path = repository_path
        self.auth = auth

        # crawl range settings.
        if crawl_start is None:
            self.crawl_start = datetime.date.today() - relativedelta(years=10)
        else:
            self.crawl_start = crawl_start
        if crawl_end is None:
            self.crawl_end = datetime.date.today()
        else:
            self.crawl_end = crawl_end

        # logger settings
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def crawl(self, limit: Optional[int] = None, interval: int = 1, force: bool = False) -> None:
        # limitが指定されている場合には取得日を制限
        date_ls = self.list_target_date(force=force)
        if limit is not None:
            size = min(len(date_ls), limit)
            date_ls = date_ls[:size]

        self.logger.info("Start crawling stock")
        success_count = 0
        fail_count = 0
        for d in date_ls:
            self.logger.info(f"Start downloading stock records of {d.strftime('%Y-%m-%d')}")
            try:
                # ダウンロードして保存
                df = jquants.download_daily_stock(self.auth.login_token, d)
                filename = d.strftime("%Y-%m-%d.csv")
                self.repository_path.save_df(rp.DIR_RAW_STOCK, filename, df)
                success_count += 1
            except Exception as e:
                fail_count += 1
                self.logger.exception(e)
                self.logger.info(f"Fail downloading {d.strftime('%Y-%m-%d')}. Error: {e}")
            time.sleep(interval)
            self.logger.info(f"Complete downloading {d.strftime('%Y-%m-%d')}")
        self.logger.info(f"Complete crawling. Successed {success_count}, Failed {fail_count}.")

    def list_target_date(self, force: bool = False) -> List[datetime.date]:
        """取得対象の日付を列挙する"""
        date_ls = workday_list(self.crawl_start, self.crawl_end)
        if force:
            return date_ls

        # 過去ダウンロードしていないデータのみダウンロードする
        already_download = []
        for filename in self.repository_path.list_dir(rp.DIR_RAW_STOCK):
            try:
                date = datetime.datetime.strptime(filename, "%Y-%m-%d.csv").date()
            except Exception as e:
                logger.exception(e)
                logger.error(f"Can not parse {filename}")
            already_download.append(date)
        date_ls = list(filter(lambda x: x not in already_download, date_ls))
        return date_ls


class MarginInterestCrawler:
    def __init__(
        self,
        repository_path: AbstractRepositoryPath,
        auth: jquants.JquantsAuthToken,
        logger: Optional[logging.Logger] = None,
        crawl_start: Optional[datetime.date] = None,
        crawl_end: Optional[datetime.date] = None,
    ) -> None:
        self.repository_path = repository_path
        self.auth = auth

        # crawl range settings.
        if crawl_start is None:
            self.crawl_start = datetime.date.today() - relativedelta(years=10)
        else:
            self.crawl_start = crawl_start
        if crawl_end is None:
            self.crawl_end = datetime.date.today()
        else:
            self.crawl_end = crawl_end

        # logger settings
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def crawl(self, limit: Optional[int] = None, interval: int = 1, force: bool = False, safety_range: int = 7) -> None:
        # limitが指定されている場合には取得日を制限
        date_ls = self.list_target_date(force, safety_range=safety_range)

        if limit is not None:
            size = min(len(date_ls), limit)
            date_ls = date_ls[:size]

        self.logger.info("Start crawling margin interests")
        success_count = 0
        fail_count = 0
        for d in date_ls:
            self.logger.info(f"Start downloading margin interest records of {d.strftime('%Y-%m-%d')}")
            try:
                # ダウンロードして保存
                df = jquants.download_daily_margin_interest(self.auth.login_token, d)
                filename = d.strftime("%Y-%m-%d.csv")
                if df is not None:
                    self.repository_path.save_df(rp.DIR_RAW_MARGIN_INTEREST, filename, df)
                else:
                    stream = io.BytesIO()
                    self.repository_path.save_stream(rp.DIR_RAW_MARGIN_INTEREST, filename, stream)
                success_count += 1
            except Exception as e:
                fail_count += 1
                self.logger.exception(e)
                self.logger.info(f"Fail to download {d.strftime('%Y-%m-%d')}. Error: {e}")
            time.sleep(interval)
            self.logger.info(f"Complete to download {d.strftime('%Y-%m-%d')}")
        self.logger.info(f"Complete crawling. Successed {success_count}, Failed {fail_count}.")

    def list_target_date(self, force: bool = False, safety_range:int = 7) -> List[datetime.date]:
        """取得対象の日付を列挙する"""
        date_ls = workday_list(self.crawl_start, self.crawl_end)
        if force:
            return date_ls

        # 過去ダウンロードしていないデータのみダウンロードする
        already_download = []
        for filename in self.repository_path.list_dir(rp.DIR_RAW_MARGIN_INTEREST):
            try:
                date = datetime.datetime.strptime(filename, "%Y-%m-%d.csv").date()
            except Exception as e:
                logger.exception(e)
                logger.error(f"Can not parse {filename}")

            if (self.crawl_end - date).days < safety_range:
                continue
            already_download.append(date)
        date_ls = list(filter(lambda x: x not in already_download, date_ls))
        return date_ls


class BrandCrawler:
    def __init__(
        self,
        repository_path: AbstractRepositoryPath,
        auth: jquants.JquantsAuthToken,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.repository_path = repository_path
        self.auth = auth
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def crawl(self) -> None:
        df = jquants.download_brand(self.auth.login_token)
        self.repository_path.save_df(rp.DIR_BRAND, "brand.csv", df)
        self.logger.info("Success to download brand.csv.")


class DailyStatementsCrawler:
    def __init__(
        self,
        repository_path: AbstractRepositoryPath,
        auth: jquants.JquantsAuthToken,
        logger: Optional[logging.Logger] = None,
        crawl_start: Optional[datetime.date] = None,
        crawl_end: Optional[datetime.date] = None,
    ) -> None:
        self.repository_path = repository_path
        self.auth = auth

        # crawl range settings.
        if crawl_start is None:
            self.crawl_start = datetime.date.today() - relativedelta(years=10)
        else:
            self.crawl_start = crawl_start
        if crawl_end is None:
            self.crawl_end = datetime.date.today()
        else:
            self.crawl_end = crawl_end

        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def crawl(self, limit: Optional[int] = None, interval: int = 1, force: bool = False, safety_range:int = 7) -> None:
        # limitが指定されている場合には取得日を制限
        date_ls = self.list_target_date(force=force, safety_range=safety_range)
        if limit is not None:
            size = min(len(date_ls), limit)
            date_ls = date_ls[:size]

        self.logger.info("Start crawling statements")
        success_count = 0
        fail_count = 0
        for d in date_ls:
            self.logger.info(f"Start downloading statements {d.strftime('%Y-%m-%d')}")
            try:
                # ダウンロードして保存
                df = jquants.download_daily_statements(self.auth.login_token, d)
                filename = d.strftime("%Y-%m-%d.csv")
                if df is not None:
                    self.repository_path.save_df(rp.DIR_RAW_STATEMENTS, filename, df)
                else:
                    stream = io.BytesIO()
                    self.repository_path.save_stream(rp.DIR_RAW_STATEMENTS, filename, stream)
                success_count += 1
            except Exception as e:
                fail_count += 1
                self.logger.info(f"Fail downloading statements {d.strftime('%Y-%m-%d')}. Error: {e}")
            time.sleep(interval)
            self.logger.info(f"Complete downloading statements {d.strftime('%Y-%m-%d')}")
        self.logger.info(f"Complete crawling. Successed {success_count}, Failed {fail_count}.")

    def list_target_date(self, force: bool = False, safety_range: int = 7) -> List[datetime.date]:
        date_ls = workday_list(self.crawl_start, self.crawl_end)
        if force:
            return date_ls

        # 過去ダウンロードしていないデータのみダウンロードする
        already_download = []
        for filename in self.repository_path.list_dir(rp.DIR_RAW_STATEMENTS):
            try:
                date = datetime.datetime.strptime(filename, "%Y-%m-%d.csv").date()
            except Exception as e:
                self.logger.warning(f"Can not parse {filename}")
                self.logger.exception(e)

            if (self.crawl_end - date).days < safety_range:
                continue
            already_download.append(date)
        date_ls = list(filter(lambda x: x not in already_download, date_ls))
        return date_ls


class YahooIndexCrawler:
    def __init__(self, repository_path: AbstractRepositoryPath, logger: Optional[logging.Logger] = None) -> None:
        self.repository_path = repository_path

    def crawl(self) -> None:

        target_pairs = [
            ("yahoo_gold", yahoo.COMODITY_GOLD),
            ("yahoo_oil", yahoo.COMODITY_CRUDE_OIL),
            ("yahoo_usd_jpy", yahoo.CURRENCY_USD_JPY),
            ("yahoo_eur_jpy", yahoo.CURRENCY_EUR_JPY),
            ("yahoo_dji", yahoo.INDEX_DJI),
            ("yahoo_sp500", yahoo.INDEX_SP500),
            ("yahoo_nikkei", yahoo.INDEX_NIKKEI),
            ("yahoo_dj_comodity", yahoo.INDEX_DJ_COMODITY),
            ("yahoo_msci_emerging", yahoo.INDEX_MSCI_EMERGING),
            ("yahoo_america_bond_5y", yahoo.BOND_AMERICA_5Y),
            ("yahoo_america_bond_10y", yahoo.BOND_AMERICA_10Y),
        ]

        start = datetime.date(2017, 1, 1)
        end = datetime.date.today()
        for name, key in target_pairs:
            try:
                logger.info(f"Downloading {key} since {start} to {end}")
                index = yahoo.download_index(key, start, end)
                repository = IndexCsvRepository(self.repository_path)
                repository.save(name, index)
            except Exception as e:
                logger.info(f"Error occrred while downloading {key}.")
                logger.exception(e)
            time.sleep(1)


def workday_list(first_date: datetime.date, last_date: datetime.date) -> List[datetime.date]:
    """営業日を列挙する"""
    d = first_date
    cal = Calendar()
    ls = []
    while d <= last_date:
        if cal.is_business_day(d):
            ls.append(d)
        d += datetime.timedelta(days=1)
    return ls


if __name__ == "__main__":
    username = os.environ["J_QUANTS_USERNAME"]
    password = os.environ["J_QUANTS_PASSWORD"]
    refresh_token = jquants.fetch_refresh_token(username, password)
    login_token = jquants.fetch_login_token(refresh_token)
    df = jquants.download_market(login_token)
