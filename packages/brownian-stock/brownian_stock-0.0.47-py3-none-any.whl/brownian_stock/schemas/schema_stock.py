from typing import Optional

from pydantic import BaseModel, StrictStr

from .types import Datetime64


class StockSchema(BaseModel):
    Date: Datetime64
    Code: StrictStr
    Close: Optional[float]
    Open: Optional[float]
    Low: Optional[float]
    High: Optional[float]
    Volume: Optional[float]
    TurnoverValue: Optional[float]
    AdjustmentFactor: Optional[float]
    AdjustmentClose: Optional[float]
    AdjustmentOpen: Optional[float]
    AdjustmentLow: Optional[float]
    AdjustmentHigh: Optional[float]
    AdjustmentVolume: Optional[float]
    UpperLimit: Optional[int]
    LowerLimit: Optional[int]
