import datetime
import json
import sys
from logging import getLogger
from typing import Optional
from urllib.parse import urljoin

import pandas as pd
import polars as pl
import requests

logger = getLogger(__name__)


def build_url(path: str) -> str:
    base_url = "https://api.jquants.com/"
    return urljoin(base_url, path)


class JquantsAuthToken:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.__refresh_token: Optional[str] = None
        self.__login_token: Optional[str] = None

    def login(self) -> None:
        logger.info(f"Try to login jquants as `{self.username}`")
        refresh_token = fetch_refresh_token(self.username, self.password)
        login_token = fetch_login_token(refresh_token)
        self.__refresh_token = refresh_token
        self.__login_token = login_token
        logger.info(f"Success to login jquants as `{self.username}`")

    def refresh(self) -> None:
        if self.__refresh_token is None:
            raise RuntimeError("Refresh token is not initialized.")
        logger.info("Refreshing jquants login token.")
        login_token = fetch_login_token(self.__refresh_token)
        self.__login_token = login_token
        logger.info("Success to refresh jquants login token.")

    @property
    def refresh_token(self) -> str:
        if self.__refresh_token is None:
            raise RuntimeError("Not Logined.")
        return self.__refresh_token

    @property
    def login_token(self) -> str:
        if self.__login_token is None:
            raise RuntimeError("Not Logined.")
        return self.__login_token


def fetch_login_token(refresh_token: str) -> str:
    """J-Quantsからlogin_tokenを取得する"""
    try:
        url = build_url(f"/v1/token/auth_refresh?refreshtoken={refresh_token}")
        r_post = requests.post(url, timeout=30)
        if r_post.status_code != 200:
            raise RuntimeError()
        token_dict = r_post.json()
        login_token = str(token_dict["idToken"])
        return login_token
    except Exception:
        raise RuntimeError("Failed to fetch login token.")


def fetch_refresh_token(username: str, password: str) -> str:
    """J-Quantsからrefresh_tokenを取得する"""
    try:
        data = {
            "mailaddress": username,
            "password": password,
        }
        url = build_url("/v1/token/auth_user")
        r_post = requests.post(url, data=json.dumps(data), timeout=30)
        if r_post.status_code != 200:
            raise RuntimeError()
        token_dict = r_post.json()
        refresh_token = str(token_dict["refreshToken"])
        return refresh_token
    except Exception:
        raise RuntimeError("Failed to fetch refresh token.")


def download_brand(login_token: str) -> pl.DataFrame:
    """利用可能な銘柄コード一覧を取得する

    Args:
        login_token(str): 認証トークン

    Returns:
        list of str: 取得した
    """
    try:
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url("/v1/listed/info")
        r = requests.get(url, headers=headers, timeout=10)
        result_dict = r.json()
    except Exception:
        raise RuntimeError("Failed to code list.")

    # 取得結果をパース
    rows = result_dict["info"]
    df = pl.DataFrame(rows)
    return df


def download_stock(login_token: str, code: str) -> pd.DataFrame:
    try:
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url(f"/v1/prices/daily_quotes?code={code}")
        r = requests.get(url, headers=headers, timeout=30)
        result_dict = r.json()

        record_ls = result_dict["daily_quotes"]
        df = pd.DataFrame(record_ls)
        return df
    except Exception:
        raise RuntimeError("Failed fetch stock information.")


def download_daily_stock(login_token: str, date: datetime.date) -> pl.DataFrame:
    try:
        date_str = date.strftime("%Y-%m-%d")
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url(f"/v1/prices/daily_quotes?date={date_str}")
        r = requests.get(url, headers=headers, timeout=30)

        result_dict = r.json()
        record_ls = result_dict["daily_quotes"]
        if len(record_ls) == 0:
            raise RuntimeError("Success to fetch, but records are blank.")
        df = pd.DataFrame(record_ls)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df[df["Date"].dt.date == date]
        return pl.from_pandas(df)
    except Exception as e:
        raise e


def download_topix(login_token: str) -> pd.DataFrame:
    """TOPIXの情報の取得"""
    try:
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url("/v1/indices/topix")
        r = requests.get(url, headers=headers)
        result_dict = r.json()
        record_ls = result_dict["topix"]
        df = pd.DataFrame(record_ls)
        return df
    except Exception:
        raise RuntimeError("Faile to fetch topix information.")


def download_statements(login_token: str, code: str) -> pl.DataFrame:
    """財務情報の取得"""
    try:
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url(f"/v1/fins/statements?code={code}")
        r = requests.get(url, headers=headers)
        result_dict = r.json()
        record_ls = result_dict["statements"]
        df = pd.DataFrame(record_ls)
        return pl.from_pandas(df)
    except Exception:
        raise RuntimeError("Failed to fetch statemnets information.")


def download_daily_statements(login_token: str, date: datetime.date) -> Optional[pl.DataFrame]:
    try:
        date_str = date.strftime("%Y-%m-%d")
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url(f"/v1/fins/statements?date={date_str}")
        r = requests.get(url, headers=headers, timeout=30)

        result_dict = r.json()
        record_ls = result_dict["statements"]
        df = pd.DataFrame(record_ls)
        if len(df) == 0:
            return None
        df["DisclosedDate"] = pd.to_datetime(df["DisclosedDate"])
        df = df[df["DisclosedDate"].dt.date == date]
        return pl.from_pandas(df)
    except Exception as e:
        raise e


def download_daily_margin_interest(login_token: str, date: datetime.date) -> Optional[pl.DataFrame]:
    try:
        date_str = date.strftime("%Y-%m-%d")
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url(f"/v1/markets/weekly_margin_interest?date={date_str}")
        r = requests.get(url, headers=headers, timeout=30)

        result_dict = r.json()
        record_ls = result_dict["weekly_margin_interest"]
        df = pd.DataFrame(record_ls)
        if len(df) == 0:
            return None

        df["Date"] = pd.to_datetime(df["Date"])
        df = df[df["Date"].dt.date == date]
        return pl.from_pandas(df)
    except Exception as e:
        raise e


def download_code_margin_interest(login_token: str, code: str) -> Optional[pl.DataFrame]:
    try:
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url(f"/v1/markets/weekly_margin_interest?code={code}")
        r = requests.get(url, headers=headers, timeout=30)

        result_dict = r.json()
        record_ls = result_dict["weekly_margin_interest"]
        df = pd.DataFrame(record_ls)
        if len(df) == 0:
            return None

        df["Date"] = pd.to_datetime(df["Date"])
        return pl.from_pandas(df)
    except Exception as e:
        raise e


def download_market(login_token: str) -> pl.DataFrame:
    try:
        headers = {"Authorization": "Bearer {}".format(login_token)}
        url = build_url("/v1/markets/trades_spec")
        r = requests.get(url, headers=headers)
        record_dict = r.json()
        record_ls = record_dict["trades_spec"]
        df = pl.DataFrame(record_ls)
        return df
    except Exception:
        raise RuntimeError("Faile to fetch market information.")


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    code = sys.argv[3]
    refresh_token = fetch_refresh_token(username, password)
    login_token = fetch_login_token(refresh_token)

    df = download_code_margin_interest(login_token, code)
    if df is None:
        raise IOError("Failed to download csv.")
    df.write_csv(f"{code}.csv")
    print(df.head())
