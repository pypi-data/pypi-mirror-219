import io
import pathlib
from abc import ABCMeta, abstractmethod, abstractproperty
from logging import getLogger
from typing import Any, List, Optional, Union

import boto3
import polars as pl

logger = getLogger(__name__)

DIR_RAW_STOCK = "raw_stock"
DIR_RAW_STATEMENTS = "raw_statements"
DIR_RAW_INDEX = "raw_index"
DIR_RAW_MARGIN_INTEREST = "raw_margin_interest"

DIR_STOCK = "stock"
DIR_STATEMENTS = "statements"
DIR_COMODITY = "comodity"
DIR_BRAND = "brand"

CSV_BRAND = "brand.csv"
CSV_TMP_BRAND = "tmp_brand.csv"
CSV_TOPIX = "topix.csv"
CSV_TMP_TOPIX = "tmp_topix.csv"


class AbstractRepositoryPath(metaclass=ABCMeta):
    @abstractproperty
    def sqlite_path(self) -> pathlib.Path:
        pass

    @abstractproperty
    def connection_str(self) -> str:
        pass

    @abstractmethod
    def list_dir(self, dir_name: str) -> List[str]:
        pass

    @abstractmethod
    def save_df(self, dir_name: str, file_name: str, df: pl.DataFrame) -> None:
        pass

    @abstractmethod
    def save_stream(self, dir_name: str, file_name: str, stream: io.BytesIO) -> None:
        pass

    @abstractmethod
    def read_df(self, dir_name: str, file_name: str) -> Optional[pl.DataFrame]:
        pass


class RepositoryPath(AbstractRepositoryPath):

    """レポジトリフォルダのパスを表現するクラス"""

    def __init__(self, dir_path: Union[str, pathlib.Path], db_connection: Optional[str] = None) -> None:
        if isinstance(dir_path, pathlib.Path):
            self.dir_path = dir_path
        elif isinstance(dir_path, str):
            self.dir_path = pathlib.Path(dir_path)
        else:
            raise TypeError("dir_path must be str or pathlib.Path object.")
        if db_connection is not None:
            self.db_connection = db_connection
        else:
            db_path = self.dir_path / "sqlite3.db"
            db_path = db_path.absolute()
            self.db_connection = "sqlite:///" + str(db_path)

    @property
    def root_path(self) -> pathlib.Path:
        """Repositoryのルートパス"""
        return self.dir_path

    @property
    def sqlite_path(self) -> pathlib.Path:
        db_path_str = self.db_connection.replace("sqlite:///", "")
        return pathlib.Path(db_path_str)

    @property
    def connection_str(self) -> str:
        return self.db_connection

    def list_dir(self, dir_name: str) -> List[str]:
        self.__bucket_check(dir_name)
        dir_path = self.dir_path / dir_name
        file_list = [f.name for f in dir_path.iterdir() if f.is_file()]
        return file_list

    def save_df(self, dir_name: str, file_name: str, df: pl.DataFrame) -> None:
        self.__bucket_check(dir_name)
        file_path = self.dir_path / dir_name / file_name
        df.write_csv(file_path, datetime_format="%Y-%m-%d")

    def save_stream(self, dir_name: str, file_name: str, stream: io.BytesIO) -> None:
        self.__bucket_check(dir_name)
        file_path = self.dir_path / dir_name / file_name
        stream.seek(0)
        with open(file_path, "wb") as fp:
            fp.write(stream.read())

    def read_df(self, dir_name: str, file_name: str) -> Optional[pl.DataFrame]:
        self.__bucket_check(dir_name)
        file_path = self.dir_path / dir_name / file_name
        if file_path.stat().st_size == 0:
            return None
        df = pl.read_csv(file_path)
        if "" in df.columns:
            df = df.drop("")
        return df

    def __bucket_check(self, bucket_name: str) -> None:
        dir_path = self.dir_path / bucket_name
        dir_path.mkdir(parents=True, exist_ok=True)


class S3RepositoryPath(AbstractRepositoryPath):
    def __init__(self, bucket_name: str, db_connection: str, region: str = "us-west-2") -> None:
        self.bucket_name = bucket_name
        self.region = region
        self.db_connection = db_connection

    @property
    def sqlite_path(self) -> pathlib.Path:
        db_path_str = self.db_connection.replace("sqlite:///", "")
        return pathlib.Path(db_path_str)

    @property
    def connection_str(self) -> str:
        return self.db_connection

    def list_dir(self, dir_name: str) -> List[str]:
        client = boto3.client("s3", region_name="ap-northeast-1")
        paginator = client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=dir_name)

        raw_file_list: List[Any] = []
        try:
            for page in page_iterator:
                if "Contents" in page:
                    page_file_ls = page["Contents"]
                    raw_file_list.extend(page_file_ls)
        except Exception as e:
            logger.exception(e)
            raise

        file_list: List[str] = []
        for file_dict in raw_file_list:
            try:
                filename = file_dict["Key"]
                if filename.endswith("/"):
                    # Direcotry Item
                    continue
                filename = filename.replace(dir_name + "/", "")
                file_list.append(filename)
            except Exception as e:
                logger.exception(e)
        return file_list

    def save_df(self, dir_name: str, file_name: str, df: pl.DataFrame) -> None:
        s3_file_name = f"{dir_name}/{file_name}"

        stream = io.BytesIO()
        df.write_csv(stream, datetime_format="%Y-%m-%d")
        stream.seek(0)

        s3 = boto3.resource("s3")
        s3.Bucket(self.bucket_name).upload_fileobj(stream, s3_file_name)

    def save_stream(self, dir_name: str, file_name: str, stream: io.BytesIO) -> None:
        s3_file_name = f"{dir_name}/{file_name}"
        stream.seek(0)
        s3 = boto3.resource("s3")
        s3.Bucket(self.bucket_name).upload_fileobj(stream, s3_file_name)

    def read_df(self, dir_name: str, file_name: str) -> Optional[pl.DataFrame]:
        s3_file_name = f"{dir_name}/{file_name}"
        stream = io.BytesIO()
        s3 = boto3.resource("s3")
        s3.Bucket(self.bucket_name).download_fileobj(s3_file_name, stream)

        if stream.getbuffer().nbytes == 0:
            return None

        df = pl.read_csv(stream)
        if "" in df.columns:
            df = df.drop("")
        return df
