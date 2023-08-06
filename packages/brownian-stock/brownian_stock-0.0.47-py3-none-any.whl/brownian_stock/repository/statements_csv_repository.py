from logging import getLogger
from typing import List, Optional

import tqdm

from ..models.statements import StatementsHistory
from . import repository_path as rp

logger = getLogger(__name__)


class StatementsCSVRepository:
    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def load(self, limit: Optional[int] = None, skip_error: bool = True) -> List[StatementsHistory]:
        """statementsディレクトリから決算情報を読み込む"""
        statements_list = []
        filelist = self.repository_path.list_dir(rp.DIR_STATEMENTS)

        if limit is not None:
            filelist = filelist[:limit]

        failed_ls = []
        for file in tqdm.tqdm(filelist):
            try:
                # CSVではなかった場合はスキップ
                if not file.name.endswith(".csv"):
                    continue
                df = self.repository_path.read_df(rp.DIR_STATEMENTS, file)
                statements = StatementsHistory(df)
                statements_list.append(statements)
            except Exception as e:
                if not skip_error:
                    raise e
                failed_ls.append(f"[*] Failed to load {file}")
        for failed_log in failed_ls:
            logger.error(failed_log)
        return statements_list

    def save(self, statements_list: List[StatementsHistory]) -> None:
        for s in tqdm.tqdm(statements_list):
            filename = f"{s.stock_code}.csv"
            self.repository_path.save_df(rp.DIR_STATEMENTS, filename, s._df)

    def log(self, msg: str) -> None:
        print(msg)


"""
def load_statements(csv_path: pathlib.Path) -> Optional[StatementsHistory]:
    if csv_path.stat().st_size == 0:
        return None
    df = pl.read_csv(csv_path)
    return StatementsHistory(df)
"""
