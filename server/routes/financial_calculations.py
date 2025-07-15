from fastapi import APIRouter, HTTPException
from utils import calculate_npv, calculate_irr, calculate_payback_period, calculate_discounted_payback, calculate_pi
from models import FinancialDetailsReq, NPVResult, SensitivityScenarios, FinancialDetailsRes, GenericError

router = APIRouter()


@router.post("/calculate-financials", response_model=FinancialDetailsRes)
async def calculate_financials(data: FinancialDetailsReq):
    
    # Baseline Values
    cash_flows = data.full_cash_flows()
    baseline_npv_1 = calculate_npv(cash_flows, data.discount_rates[0])
    baseline_npv_2 = calculate_npv(cash_flows, data.discount_rates[1])
    baseline_irr = calculate_irr(cash_flows)
    baseline_payback_period = calculate_payback_period(cash_flows)
    baseline_discounted_payback_1 = calculate_discounted_payback(cash_flows, data.discount_rates[0])
    baseline_discounted_payback_2 = calculate_discounted_payback(cash_flows, data.discount_rates[1])
    baseline_pi_1 = calculate_pi(cash_flows, data.discount_rates[0])
    baseline_pi_2 = calculate_pi(cash_flows, data.discount_rates[1])

    # Pessimistic Values
    pessimistic_capex = data.investment * (1 + data.capex_adjustments[0])
    pessimistic_cash_flows = [-pessimistic_capex] + data.cash_flows
    pessimistic_npv_1 = calculate_npv(pessimistic_cash_flows, data.discount_rates[0])
    pessimistic_npv_2 = calculate_npv(pessimistic_cash_flows, data.discount_rates[1])
    pessimistic_irr = calculate_irr(pessimistic_cash_flows)
    pessimistic_payback_period = calculate_payback_period(pessimistic_cash_flows)
    pessimistic_discounted_payback_1 = calculate_discounted_payback(pessimistic_cash_flows, data.discount_rates[0])
    pessimistic_discounted_payback_2 = calculate_discounted_payback(pessimistic_cash_flows, data.discount_rates[1])
    pessimistic_pi_1 = calculate_pi(pessimistic_cash_flows, data.discount_rates[0])
    pessimistic_pi_2 = calculate_pi(pessimistic_cash_flows, data.discount_rates[1])

    # Optimistic Values
    optimistic_capex = data.investment * (1 - data.capex_adjustments[1])
    optimistic_cash_flows = [-optimistic_capex] + data.cash_flows
    optimistic_npv_1 = calculate_npv(optimistic_cash_flows, data.discount_rates[0])
    optimistic_npv_2 = calculate_npv(optimistic_cash_flows, data.discount_rates[1])
    optimistic_irr = calculate_irr(optimistic_cash_flows)
    optimistic_payback_period = calculate_payback_period(optimistic_cash_flows)
    optimistic_discounted_payback_1 = calculate_discounted_payback(optimistic_cash_flows, data.discount_rates[0])
    optimistic_discounted_payback_2 = calculate_discounted_payback(optimistic_cash_flows, data.discount_rates[1])
    optimistic_pi_1 = calculate_pi(optimistic_cash_flows, data.discount_rates[0])
    optimistic_pi_2 = calculate_pi(optimistic_cash_flows, data.discount_rates[1])



    return FinancialDetailsRes(

        npv_results = [
            NPVResult(
                discount_rate = data.discount_rates[0],
                npv = baseline_npv_1,
                pi = baseline_pi_1
            ),

            NPVResult(
                discount_rate = data.discount_rates[1],
                npv = baseline_npv_2,
                pi = baseline_pi_2
            )
        ],


        irr = baseline_irr,
        payback_period = baseline_payback_period,
        discounted_paybacks = [baseline_discounted_payback_1, baseline_discounted_payback_2],


        sensitivity_analysis = [

            SensitivityScenarios(
                capex_adjustment = data.capex_adjustments[0],
                npv_results = [
                    NPVResult(
                        discount_rate = data.discount_rates[0],
                        npv = pessimistic_npv_1,
                        pi = pessimistic_pi_1
                    ),
                    NPVResult(
                        discount_rate = data.discount_rates[1],
                        npv = pessimistic_npv_2,
                        pi = pessimistic_pi_2
                    )
                ],
                irr = pessimistic_irr,
                payback_period = pessimistic_payback_period,
                discounted_paybacks = [pessimistic_discounted_payback_1, pessimistic_discounted_payback_2]
            ),

            SensitivityScenarios(
                capex_adjustment = data.capex_adjustments[1],
                npv_results = [
                    NPVResult(
                        discount_rate = data.discount_rates[0],
                        npv = optimistic_npv_1,
                        pi = optimistic_pi_1
                    ),
                    NPVResult(
                        discount_rate = data.discount_rates[1],
                        npv = optimistic_npv_2,
                        pi = optimistic_pi_2
                    )
                ],


                irr = optimistic_irr,
                payback_period = optimistic_payback_period,
                discounted_paybacks = [optimistic_discounted_payback_1, optimistic_discounted_payback_2]
            )
        ]

    )
