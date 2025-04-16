from typing import List, Optional
from pydantic import BaseModel

class NPVRequest(BaseModel):
    discount_rate: float
    cash_flows: List[int]

class NPVResponse(BaseModel):
    npv: int

class IRRRequest(BaseModel):
    cash_flows: List[int]
    
class IRRResponse(BaseModel):
    irr: int

class PaybackPeriodRequest(BaseModel):
    initial_investment: int
    cash_flows: List[int]

class PaybackPeriodResponse(BaseModel):
    payback_period: Optional[float]

class DiscountedPaybackPeriodRequest(PaybackPeriodRequest):
    discount_rate: float
    
class DiscountedPaybackPeriodResponse(PaybackPeriodRequest):
    discounted_payback_period: Optional[float]
    
class NPVAnalysisRequest(DiscountedPaybackPeriodRequest):
    capex_increase: float

class NPVAnalysisResponse(BaseModel):
    npv: int

    