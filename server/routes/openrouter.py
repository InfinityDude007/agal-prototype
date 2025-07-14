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

    # Titles, instructions and data for report sections to prompt with
    report_sections = [
        ("Executive Summary", "Write a short, compelling summary highlighting overall project feasibility, based on the inputs."),
        ("Introduction & Methodology", "Explain the project goal, its strategic context, and relevance to the industry and country. Describe how you will evaluate the project (financial models, assumptions, benchmarks, etc.)."),
        ("Financial Forecasting, DCF & Capital Budgeting", "Using the realistic numbers, assumptions, forecast production, revenue, and costs, make a financial forecast. Compute and explain DCF, IRR, NPV, Payback Periods using time value of money assumptions."),
        ("Sensitivity Analysis & Recommendations", "Analyze risk using scenarios where capex or prices shift +/-10%. Provide a final assessment of the project, including action items and takeaways."),
    ]

    inference_time = 0
    previous_sections = ""
    for title, instruction in report_sections:

    # Setup model prompt from skeleton prompt, sections and user details
        prompt = f"""
            You are a professional financial analyst. Write a detailed markdown report evaluating the viability of a project based on the inputs below. The tone should match that of a corporate finance feasibility report for senior executives (similar to McKinsey, PwC, or MNC internal reporting). The output must include clear headings and structured analysis.

            ---
            
            Previous content:
            {previous_sections}

            ---
            
            Project Input
            - Project Type: {details.project_type}
            - Project Goal: {details.project_goal}
            - Industry: {details.company_industry}
            - Investment Amount: {details.investment}
            - Prospective Countries: {details.countries}
            
            ---

            General Instructions:
            - Use realistic numbers and economic reasoning.
            - Prioritize depth over length where needed.
            - Use tables where appropriate to visualise numerical data.
            - Avoid using table for non-numerical details.
            - Return a full markdown formatted response.
            - Stick to the formatting and font sizing of previous sections, ensuring visual and logical consistency while avoiding repetition.

            Format Rules:
            - Do NOT repeat the main report title aside from the start (before the executive summary section).
            - Start the section with a heading using `--- ## Title` (e.g. "Conclusion").
            - Use `###` for subheadings (e.g., "Recommendation").
            - Do NOT center text or add custom markdown styles.

            Final report structure and sections:
            1. Main Title: "Project Viability Analysis: [rephrase of project_type + industry]"
            2. Executive Summary: Summarize key findings, most viable country, and recommendation.
            3. Introduction: Expand the project context and strategic goal.
            4. Methodology: State financial assumptions (e.g., CAGR, labour cost, government incentives) and analysis methods (e.g., geographical, tax, risk).
            5. Key Considerations:
                - Geographical Advantages
                - Tax Considerations
                - Market Demand
                - Economic Factors
            6. Sensitivity Analysis: Briefly assess 3 to 4 risks (e.g., supply chain, regulation, CAPEX) and possible mitigations.
            7. Conclusion & Recommendations: Summarize findings and list 3 to 4 bullet-point action items.

            ---

            You are writing the following sections of the report:
            Section: {title}
            Instruction: {instruction}

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


        # Make call to Openrouter and record response section
        timeout = httpx.Timeout(90.0, connect=10.0)
        t0 = time.time()
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(API_URL, json=data, headers=headers)
        t1 = time.time()


        if response.status_code == 200:
            full_response = response.json()
            raw_content = full_response["choices"][0]["message"]["content"]
            content = sanitize_md(raw_content)
            previous_sections += f"\n\n{content.strip()}\n"
            inference_time += t1-t0
        
        else:
            raise HTTPException(
                status_code=502,
                detail={
                    "error": f"Failed to fetch data from Openrouter API at section: {title}",
                    "status_code": response.status_code,
                    "details": response.text
                }
            )
        
    
    # Return final response
    if previous_sections:
        return ProjectDetailsRes(
                model_response=previous_sections,
                inference_time=f"{inference_time:.2f} seconds"
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
