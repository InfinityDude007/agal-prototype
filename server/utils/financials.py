import numpy_financial as npf
from typing import List


def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    return npf.npv(discount_rate, cash_flows[1:]) + cash_flows[0]


def calculate_irr(cash_flows: List[float]) -> float:
    return npf.irr(cash_flows)


def calculate_payback_period(cash_flows: List[float]) -> float:
    cumulative = 0
    payback_period = 0

    for i, cf in enumerate(cash_flows, 1):
        cumulative += cf
        if cumulative >= abs(cash_flows[0]):
            payback_period = i - 1 + (abs(cash_flows[0]) - (cumulative - cf)) / cf
            break

    return payback_period


def calculate_discounted_payback(cash_flows: List[float], discount_rate: float) -> float:
    discounted_cash_flows = [cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows[1:], 1)]
    cumulative = 0
    discounted_payback = 0

    for i, dcf in enumerate(discounted_cash_flows, 1):
        cumulative += dcf
        if cumulative >= abs(cash_flows[0]):
            discounted_payback = i - 1 + (abs(cash_flows[0]) - (cumulative - dcf)) / dcf
            break

    return discounted_payback


def calculate_pi(cash_flows: List[float], discount_rate: float) -> float:
    pv_future_cash = calculate_npv(cash_flows, discount_rate)
    return (pv_future_cash / abs(cash_flows[0]))
