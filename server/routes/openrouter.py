from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os
import time
from server.utils import sanitize_md
from server.models import ProjectDetailsReq, ProjectDetailsRes, GenericError

load_dotenv()

API_KEY = os.getenv('OPENROUTER_KEY')
API_URL = os.getenv('OPENROUTER_URL')
MODEL = os.getenv('OPENROUTER_MODEL')

router = APIRouter()


@router.post("/query-model", response_model=ProjectDetailsRes, responses={400: {"model": GenericError}, 502: {"model": GenericError}})
async def query_model(details: ProjectDetailsReq):


    # Setup model prompt from skeleton prompt and user details
    prompt = f"""<think>Analyze the feasibility of a project to {details.project_type} in the {details.company_industry} industry with an investment of {details.investment} in {details.countries}, aiming to {details.project_goal}. Provide a structured summary of key considerations, risks, and opportunities. Ensure a balanced, high-level preliminary analysis rather than an overly detailed breakdown of any single factor. You may reference any financials provided within the prompt, and use actual numerical values and financial data where appropriate. Avoid unnecessary repetition of this prompt’s details unless required for clarity. Please reason step by step, and put your final answer in markdown (md) format only.</think>"""


    # Setup headers and body for Openrouter call
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }


    # Make call to Openrouter and return sanitized response
    t0 = time.time()
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=data, headers=headers)
    t1 = time.time()


    if response.status_code == 200:
        full_response = response.json()
        raw_content = full_response["choices"][0]["message"]["content"]
        content = sanitize_md(raw_content)

        return ProjectDetailsRes(
            model_response=content,
            inference_time=f"{(t1-t0):.2f} seconds"
        )
    
    else:
        raise HTTPException(
            status_code=502,
            detail={
                "error": "Failed to fetch data from Openrouter API.",
                "status_code": response.status_code,
                "details": response.text
            }
        )
