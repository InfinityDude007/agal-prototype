import os

# Suppress cuDNN/cuBLAS warnings and optimise GPU usage
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"
os.environ["CUDA_MODULE_LOADING"] = "LAZY"
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
os.environ["SDPA_ALLOW_SLIDING_WINDOW"] = "1"
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128' 

import sys
import time
import torch
import threading
from schema.model_schema import ProjectDetails, GeneratedPrompt, ModelResponse
from transformers import AutoModelForCausalLM, AutoTokenizer


###########################################################################################################################################################################################################################################


# Model to be used
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"


# Set max tokens and model temperature
tokens_config = 1500
temp_config = 0.6


# Check if GPU is available and set device
device = "cuda" if torch.cuda.is_available() else "cpu"


###########################################################################################################################################################################################################################################



def update_elapsed_time(start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        sys.stdout.write(f"\rTime Elapsed: {int(minutes):02}:{int(seconds):02}")
        sys.stdout.flush()
        time.sleep(1)



###########################################################################################################################################################################################################################################



def load_model():
    print(f"\nModel: {model_name.split('/')[1]}\nLoading model on {device.upper()}...\n")

    start_time = time.time()
    stop_event = threading.Event()
    elapsed_time_thread = threading.Thread(target=update_elapsed_time, args=(start_time, stop_event))
    elapsed_time_thread.daemon = True
    elapsed_time_thread.start()

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)

    stop_event.set()
    elapsed_time_thread.join()
    
    elapsed_time = (time.time() - start_time) - 1
    print(f"\n\n\nModel: {model_name.split('/')[1]}\nLoaded model on {device.upper()} ✅\n")
    minutes, seconds = divmod(elapsed_time, 60)
    sys.stdout.write(f"\rTime to Load: {int(minutes):02}:{int(seconds):02}")


    return tokenizer, model

tokenizer, model = load_model()



###########################################################################################################################################################################################################################################



def get_details() -> ProjectDetails:

    print("Enter project details\n\n")
    project_type = input("Project type: ")
    project_goal = input("Project goal: ")
    company_industry = input("Industry: ")
    investment = input("Investment amount: ")
    countries = input("Short listed countries: ")

    return ProjectDetails (
            project_type=project_type,
            project_goal=project_goal,
            company_industry=company_industry,
            investment=investment,
            countries=countries
        )



###########################################################################################################################################################################################################################################



def generate_prompt(details: ProjectDetails) -> GeneratedPrompt:

    prompt = f"""<think>\nAnalyze the feasibility of a project to {details.project_type} in the {details.company_industry} industry with an investment of {details.investment} in {details.countries}, aiming to {details.project_goal}. 
\nProvide a structured summary of key considerations, risks, and opportunities. 
\nEnsure a balanced, high-level preliminary analysis rather than an overly detailed breakdown of any single factor.
\nYou may reference any financials provided within the prompt, and use actual numerical values and financial data where appropriate.
\nAvoid unnecessary repetition of this prompt’s details unless required for clarity. 
\nPlease reason step by step, and put your final answer within \\boxed{{}}
\n</think>"""

    return GeneratedPrompt(
        prompt=prompt
    )



###########################################################################################################################################################################################################################################



def call_llm(generated_prompt: GeneratedPrompt) -> ModelResponse:
    print("Awaiting model response...\n")
    start_time = time.time()

    stop_event = threading.Event()
    elapsed_time_thread = threading.Thread(target=update_elapsed_time, args=(start_time, stop_event))
    elapsed_time_thread.daemon = True
    elapsed_time_thread.start()

    inputs = tokenizer(generated_prompt.prompt, return_tensors="pt").to(device)
    response = model.generate(
        **inputs, 
        max_new_tokens=tokens_config, 
        temperature=temp_config, 
        pad_token_id=tokenizer.eos_token_id
    )

    stop_event.set()
    elapsed_time_thread.join()

    return ModelResponse(
        response=tokenizer.decode(response[0], skip_special_tokens=True),
        time_elapsed=(time.time() - start_time) - 1
    )



###########################################################################################################################################################################################################################################



def model_response_to_md(model_response: ModelResponse):
    
    if "</think>" in model_response.response:
        cleaned_response = "# Model Response\n" + model_response.response.split("</think>", 1)[1]
    else:
        cleaned_response = "# Model Response\n" + model_response.response

    minutes, seconds = divmod(model_response.time_elapsed, 60)
    time_string = f"## Response Time: {int(minutes):02}:{int(seconds):02}"
    
    file_name = "model_response.md"

    with open(file_name, "w") as file:
        file.write(f"{time_string}\n\n{cleaned_response}")

    print(f"\n{file_name} has been updated with the cleaned model response and response time ✅\n")
