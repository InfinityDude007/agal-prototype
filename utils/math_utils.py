import numpy as np
import numpy_financial as npf


###########################################################################################################################################################################################################################################


def calculate_npv(discount_rate, cash_flows):
    npv = npf.npv(discount_rate, cash_flows)
    return int(npv)


###########################################################################################################################################################################################################################################


def calculate_irr(cash_flows):
    irr = np.round(npf.irr(cash_flows), 2)
    irr_as_percentage = irr * 100
    return int(irr_as_percentage)


###########################################################################################################################################################################################################################################


def calculate_payback_period(initial_investment, cash_flows):
    cumulative = 0
    for i, cf in enumerate(cash_flows, 1):
        cumulative += cf
        if cumulative >= initial_investment:
            return np.round((i - 1 + (initial_investment - (cumulative - cf)) / cf), 9)
    
    return None


###########################################################################################################################################################################################################################################


def discounted_payback_period(initial_investment, cash_flows, discount_rate):
    discounted_cash_flows = [cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows, 1)]
    cumulative = 0
    discounted_payback = 0

    for i, dcf in enumerate(discounted_cash_flows, 1):
        cumulative += dcf
        if cumulative >= initial_investment:
            discounted_payback = i - 1 + (initial_investment - (cumulative - dcf)) / dcf
            break

    return round(discounted_payback, 9)


###########################################################################################################################################################################################################################################


def npv_analysis(cash_flows, initial_investment, discount_rate, capex_increase):
    capex = initial_investment * capex_increase
    npv = npf.npv(discount_rate, cash_flows[1:]) - capex
    return round(npv, 2)


###########################################################################################################################################################################################################################################


def profitability_index(initial_investment, cash_flows, discount_rate):
    pv_future_cash = calculate_npv(discount_rate, cash_flows) + abs(initial_investment)
    pi = int(pv_future_cash) / abs(initial_investment)
    return np.round(pi, 2)
