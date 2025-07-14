from pydantic import BaseModel
from typing import List


class FinancialDetailsReq(BaseModel):
    investment: int
    cash_flows: List[float]
    discount_rates: List[float]
    capex_adjustments: List[float]

    def full_cash_flows(self) -> List[float]:
        return [-self.investment] + self.cash_flows


class NPVResult(BaseModel):
    discount_rate: float
    npv: float
    pi: float


class SensitivityScenarios(BaseModel):
    capex_adjustment: float
    npv_results: List[NPVResult]
    irr: float
    payback_period: float
    discounted_paybacks: List[float]


class FinancialDetailsRes(BaseModel):
    npv_results: List[NPVResult]
    irr: float
    payback_period: float
    discounted_paybacks: List[float]
    sensitivity_analysis: List[SensitivityScenarios]
