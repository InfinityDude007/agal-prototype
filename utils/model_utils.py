import sys
import time
import torch
from typing import Dict
from transformers import AutoModelForCausalLM, AutoTokenizer 



# Model to be used
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

# Set max tokens and model temperature
tokens_config = 800
temp_config = 0.6



def load_model():
    
    print(f"\nModel: {model_name.split('/')[1]}\nLoading model...\n")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)   
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    ).to(device)

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
\nYou may reference any financials provided within the prompt, and use actual numerical values and financial data where appropriate.
\nAvoid unnecessary repetition of this prompt’s details unless required for clarity. 
\nPlease reason step by step, and put your final answer within \\boxed{{}}
\n</think>"""

    return prompt



def call_llm(prompt: str) -> str:
    
    print("Awaiting model response...\n")

    start_time = time.time()
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    response = model.generate(
        **inputs, 
        max_new_tokens=tokens_config, 
        temperature=temp_config, 
        pad_token_id=tokenizer.eos_token_id
    )

    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    sys.stdout.write(f"\rElapsed Time: {int(minutes):02}:{int(seconds):02}")
    sys.stdout.flush()

    return tokenizer.decode(response[0], skip_special_tokens=True), elapsed_time



def model_response_to_md(model_response: str, elapsed_time: float):

    cleaned_response = "/**Model Response**/\n" + model_response.split("</think>")[1]
    minutes, seconds = divmod(elapsed_time, 60)
    time_string = f"Elapsed Time: {int(minutes):02}:{int(seconds):02}"
    
    file_name = "model_response.md"

    with open(file_name, "w") as file:
        file.write(f"{time_string}\n\n{cleaned_response}")

    print(f"{file_name} has been updated with the cleaned model response and elapsed time\n")
