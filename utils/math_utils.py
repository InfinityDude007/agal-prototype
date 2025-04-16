import numpy as np
import numpy_financial as npf
from schema.math_schema import NPVRequest, NPVResponse, IRRRequest, IRRResponse, PaybackPeriodRequest, PaybackPeriodResponse,DiscountedPaybackPeriodRequest, DiscountedPaybackPeriodResponse, NPVAnalysisRequest, NPVAnalysisResponse


###########################################################################################################################################################################################################################################


def calculate_npv(npv_values: NPVRequest) -> NPVResponse:
    npv = npf.npv(npv_values.discount_rate, npv_values.cash_flows)
    return NPVResponse(
        npv=int(npv)
    )


###########################################################################################################################################################################################################################################


def calculate_irr(irr_values: IRRRequest) -> IRRResponse:
    irr = np.round(npf.irr(irr_values.cash_flows), 2)
    irr_as_percentage = irr * 100
    return IRRResponse(
        irr=irr_as_percentage
    )


###########################################################################################################################################################################################################################################


def calculate_payback_period(payback_period_values: PaybackPeriodRequest) -> PaybackPeriodResponse:
    cumulative = 0
    for i, cf in enumerate(payback_period_values.cash_flows, 1):
        cumulative += cf
        if cumulative >= payback_period_values.initial_investment:
            payback_period = np.round((i - 1 + (payback_period_values.initial_investment - (cumulative - cf)) / cf), 9)
            return PaybackPeriodResponse(
                payback_period=payback_period
            )
    return None


###########################################################################################################################################################################################################################################


def discounted_payback_period( discounted_payback_period_values: DiscountedPaybackPeriodRequest) -> DiscountedPaybackPeriodResponse:
    discounted_cash_flows = [cf / (1 + discounted_payback_period_values.discount_rate) ** i for i, cf in enumerate(discounted_payback_period_values.cash_flows, 1)]
    cumulative = 0
    discounted_payback = 0

    for i, dcf in enumerate(discounted_cash_flows, 1):
        cumulative += dcf
        if cumulative >= discounted_payback_period_values.initial_investment:
            discounted_payback = i - 1 + (discounted_payback_period_values.initial_investment - (cumulative - dcf)) / dcf
            break

    return DiscountedPaybackPeriodResponse(
        discounted_payback_period = np.round(discounted_payback, 2)
    )


###########################################################################################################################################################################################################################################


def npv_analysis(npv_analysis_values: NPVAnalysisRequest) -> NPVAnalysisResponse:
    capex = npv_analysis_values.initial_investment * npv_analysis_values.capex_increase
    npv = npf.npv(npv_analysis_values.discount_rate, npv_analysis_values.cash_flows[1:]) - capex
    return NPVAnalysisResponse(
        npv = np.round(npv, 2)
    )


###########################################################################################################################################################################################################################################


def profitability_index(profatibiliy_index_values: DiscountedPaybackPeriodRequest) -> DiscountedPaybackPeriodRequest:
    pv_future_cash = calculate_npv(profatibiliy_index_values.discount_rate, profatibiliy_index_values.cash_flows) + abs(profatibiliy_index_values.initial_investment)
    pi = int(pv_future_cash) / abs(profatibiliy_index_values.initial_investment)
    return DiscountedPaybackPeriodResponse(
        pi = np.round(pi, 2)
    )
