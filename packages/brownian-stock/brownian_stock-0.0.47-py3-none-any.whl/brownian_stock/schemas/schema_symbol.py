from typing import Optional

from pydantic import BaseModel, StrictStr

from .types import Datetime64


class SymbolSchema(BaseModel):
    Date: Datetime64
    Code: StrictStr
    CompanyName: str
    CompanyNameEnglish: str
    Sector17Code: str
    Sector17CodeName: str
    Sector33Code: str
    Sector33CodeName: str
    ScaleCategory: Optional[str]
    MarketCode: str
    MarketCodeName: str
    MarginCode: str
    MarginCodeName: str
