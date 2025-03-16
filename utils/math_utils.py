import numpy as np
from numpy_financial import irr

def calculate_npv(discount_rate, cash_flows):
    npv = np.npv(discount_rate, cash_flows[1:]) + cash_flows[0]
    return npv


def calculate_irr(cash_flows):
    return irr(cash_flows) 


def calculate_payback_period(initial_investment, cash_flows):
    cumulative = 0
    for i, cf in enumerate(cash_flows, 1):
        cumulative += cf
        if cumulative >= initial_investment:
            return i - 1 + (initial_investment - (cumulative - cf)) / cf  # Fractional year calculation
    
    return None


def discounted_payback_period(cash_flows, initial_investment, discount_rate=0.08):
    discounted_cash_flows = [cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows, 1)]
    cumulative = 0
    discounted_payback = 0

    for i, dcf in enumerate(discounted_cash_flows, 1):
        cumulative += dcf
        if cumulative >= initial_investment:
            discounted_payback = i - 1 + (initial_investment - (cumulative - dcf)) / dcf
            break

    return round(discounted_payback, 2)


def npv_analysis(cash_flows, initial_investment, discount_rate=0.08, capex_increase=1.2):
    capex_pessimistic = initial_investment * capex_increase
    npv_pessimistic = np.npv(discount_rate, cash_flows[1:]) - capex_pessimistic
    return round(npv_pessimistic, 2)


def profitability_index(cash_flows, initial_investment, discount_rate=0.08):
    pv_future_cash = np.npv(discount_rate, cash_flows)
    pi = pv_future_cash / abs(initial_investment)
    return round(pi, 2)