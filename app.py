from model_config import llm_client
from utils.model_utils import get_details, generate_prompt, call_llm
from utils.math_utils import *
print("\n\n---- AGAL Initial Analysis Prototype ----\n\n")

details = get_details()


# Prompt dictionary for testing

test_details = {
    "project_type": "build a new factory",
    "project_goal": "increase revenue, production capacity, outreach and market share",
    "company_industry": "electric vehicles, mainly cars",
    "investment": "5,000,000,000 ",
    "countries": "France, Germany, India or USA",
    "cash_flows": [5e9, 758e6, 1.56e9, 2.76e9, 2.48e9, 2.71e9, 2.73e9, 3.03e9, 2.86e9, 2.86e9, 2.91e9],
    "discount_rate":"0.8"
}



prompt = generate_prompt(details)

model_response = call_llm(llm_client, prompt)

print(f"\n\nModel response: {model_response}\n\n")

print(calculate_npv(test_details.get("discount_rate"), test_details.get("cash_flows")))
