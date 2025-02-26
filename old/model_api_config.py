### OLD CODE: INTENDED FOR USING HUGGINGFACE API ###
"""
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()
api_key = os.getenv('HUGGINGFACE_API_KEY')


repo_id = "microsoft/Phi-3-mini-4k-instruct"
llm_client = InferenceClient(
    model=repo_id,
    token=api_key,
    timeout=120,
)

tokens_config = 1000
temp_config = 0.4
"""
