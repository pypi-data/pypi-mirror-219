from typing import Optional

from pydantic import BaseModel, StrictStr

from .types import Datetime64


class MarginInterestSchema(BaseModel):
    Date: Datetime64
    Code: StrictStr
    ShortMarginTradeVolume: Optional[float]
    LongMarginTradeVolume: Optional[float]
    ShortNegotiableMarginTradeVolume: Optional[float]
    LongNegotiableMarginTradeVolume: Optional[float]
    ShortStandardizedMarginTradeVolume: Optional[float]
    LongStandardizedMarginTradeVolume: Optional[float]
    IssueType: int
