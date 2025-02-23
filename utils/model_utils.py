from typing import Dict
from model_config import tokens_config, temp_config
from huggingface_hub import InferenceClient


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

    prompt = f"""Analyze the feasibility a project to {details["project_type"]} in the {details["company_industry"]} industry with an investment of 
{details["investment"]} in {details["countries"]}, in order to {details["project_goal"]}.

Provide a summary of key considerations, risks, and opportunities.

Ensure your response is less than 500 tokens (3000 characters).
Avoid going super in-depth during your response, avoiding focus on only one key element and instead providing a birds-eye-view preliminary analysis.
Avoid repeating information from this prompt in your response unless necessary to provide relevant context."""

    return prompt


def call_llm(inference_client: InferenceClient, prompt: str) -> str:

    response = inference_client.text_generation(
        prompt,
        max_new_tokens=tokens_config,
        temperature=temp_config
        )
    
    return response
