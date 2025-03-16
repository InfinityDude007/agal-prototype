import os
import sys
from IPython.display import clear_output
from schema.model_schema import ProjectDetails
from utils.model_utils import get_details, generate_prompt, call_llm, model_response_to_md


# Ignore Hugging Face Hub's symlinks caching and spda warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
sys.stderr = open(os.devnull, 'w')
sys.stdout.write("Forcing warnings to be suppressed.")
clear_output(wait=True)
sys.stderr = sys.__stderr__

print("\n\n---- AGAL Initial Prototype ----\n\n")


"""
details = get_details()
"""

### DICTIONARY FOR TESTING ONLY ###

test_details = ProjectDetails(
    project_type="build a new factory",
    project_goal="increase revenue, production capacity, outreach and market share",
    company_industry="electric vehicles, mainly cars",
    investment="5,000,000,000 euros",
    countries="France, Germany, or USA"
)


prompt = generate_prompt(test_details)

model_response = call_llm(prompt)

model_response_to_md(model_response)
