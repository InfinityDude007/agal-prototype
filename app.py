from model_config import llm_client
from utils.model_utils import get_details, generate_prompt, call_llm

print("\n\n---- AGAL Initial Analysis Prototype ----\n\n")

details = get_details()


# Prompt dictionary for testing
"""
test_details = {
    "project_type": "build a new factory",
    "project_goal": "increase revenue, production capacity, outreach and market share",
    "company_industry": "electric vehicles, mainly cars",
    "investment": "5,000,000,000 euros",
    "countries": "France, Germany, India or USA"
}
"""


prompt = generate_prompt(details)

model_response = call_llm(llm_client, prompt)

print(f"\n\nModel response: {model_response}\n\n")
