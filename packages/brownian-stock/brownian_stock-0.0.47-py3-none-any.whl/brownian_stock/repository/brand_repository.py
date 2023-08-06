from typing import List

import polars as pl

from ..models.brand import Brand
from ..schemas import SymbolSchema, cast
from . import repository_path as rp


class BrandRepository:
    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def load(self) -> List[Brand]:
        brand_ls = []
        conn = self.repository_path.connection_str
        brand_df = pl.read_sql("SELECT * FROM brand;", conn).to_pandas()
        brand_df = cast(brand_df, SymbolSchema)
        for _, row in brand_df.iterrows():
            code = row["Code"]
            company_name = row["CompanyName"]
            company_name_english = row["CompanyNameEnglish"]
            sector17 = row["Sector17Code"]
            sector33 = row["Sector33Code"]
            scale_category = row["ScaleCategory"]
            market_code = row["MarketCode"]
            margin_code = row["MarginCode"]
            brand = Brand(
                code=code,
                company_name=company_name,
                company_name_english=company_name_english,
                sector17=sector17,
                sector33=sector33,
                scale_category=scale_category,
                market_code=market_code,
                margin_code=margin_code,
            )
            brand_ls.append(brand)
        return brand_ls
