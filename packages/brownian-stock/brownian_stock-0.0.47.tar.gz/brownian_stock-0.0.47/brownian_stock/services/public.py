"""
外部に公開する処理群
ユーザーが使いやすいような形式で提供する
"""

from .. import StockSet, repository


def load_stock(repo_path: repository.RepositoryPath, **kwargs) -> StockSet:
    repo = repository.StockSQLRepository(repo_path)
    stock_set = repo.load()
    return stock_set
