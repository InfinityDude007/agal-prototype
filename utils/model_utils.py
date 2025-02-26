import torch
from typing import Dict
from transformers import AutoModelForCausalLM, AutoTokenizer 



# Model to be used
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"

# Set max tokens and model temperature
tokens_config = 3000
temp_config = 0.6



def load_model():

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to(device)

    return tokenizer, model, device

tokenizer, model, device = load_model()


def get_details() -> Dict[str, str]:

    print("Enter project details\n\n")
    project_type = input("Project type: ")
    project_goal= input("Project goal: ")
    company_industry = input("Industry: ")
    investment = input("Investment amount: ")
    countries = input("Short listed countries: ")

    return {
        "project_type": project_type,
        "project_goal": project_goal,
        "company_industry": company_industry,
        "investment": investment,
        "countries": countries
    }


def generate_prompt(details: Dict[str, str]) -> str:

    prompt = f"""<think>\nAnalyze the feasibility of a project to {details['project_type']} in the {details['company_industry']} industry with an investment of {details['investment']} in {details['countries']}, aiming to {details['project_goal']}. 
\nProvide a structured summary of key considerations, risks, and opportunities. 
\nEnsure a balanced, high-level preliminary analysis rather than an overly detailed breakdown of any single factor.
\nAvoid unnecessary repetition of this prompt’s details unless required for clarity. 
\nPlease reason step by step, and put your final answer within \\boxed{{}}"""

    return prompt


def call_llm(prompt: str) -> str:
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    response = model.generate(**inputs, max_new_tokens=tokens_config, temperature=temp_config)

    return tokenizer.decode(response[0], skip_special_tokens=True)
