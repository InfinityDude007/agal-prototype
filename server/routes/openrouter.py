from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os
import time
from utils import sanitize_md
from models import ProjectDetailsReq, ProjectDetailsRes, GenericError

load_dotenv()

API_KEY = os.getenv('OPENROUTER_KEY')
API_URL = os.getenv('OPENROUTER_URL')
MODEL = os.getenv('OPENROUTER_MODEL')

router = APIRouter()


@router.post("/query-model", response_model=ProjectDetailsRes, responses={400: {"model": GenericError}, 502: {"model": GenericError}})
async def query_model(details: ProjectDetailsReq):


    # Setup model prompt from skeleton prompt and user details
    prompt = f"""
        You are a professional financial analyst. Write a detailed markdown report evaluating the viability of a project based on the inputs below. The tone should match that of a corporate finance feasibility report for senior executives (similar to McKinsey, PwC, or MNC internal reporting). The output must include clear headings and structured analysis.
        
        ---
        
        Project Input
        - Project Type: {details.project_type}
        - Project Goal: {details.project_goal}
        - Industry: {details.company_industry}
        - Investment Amount: {details.investment}
        - Prospective Countries: {details.countries}
        
        ---
        
        Output Requirements:
        1. Title: "Project Viability Analysis: [rephrase of project_type + industry]"
        2. Executive Summary: Summarize key findings, most viable country, and recommendation.
        3. Introduction: Expand the project context and strategic goal.
        4. Methodology: State financial assumptions (e.g., CAGR, labour cost, government incentives) and analysis methods (e.g., geographical, tax, risk).
        5. Key Considerations (format with markdown tables):
            - Geographical Advantages
            - Tax Considerations
            - Market Demand
            - Economic Factors
        6. Sensitivity Analysis: Briefly assess 3–4 risks (e.g., supply chain, regulation, CAPEX) and possible mitigations.
        7. Conclusion & Recommendations: Summarize findings and list 3–4 bullet-point action items.
        
        Use realistic numbers and economic reasoning. Prioritize depth over length where needed. Return a full markdown formatted response.
    """


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
