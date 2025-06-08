from pydantic import BaseModel

class ProjectDetailsReq(BaseModel):
    project_type: str
    project_goal: str
    company_industry: str
    investment: str
    countries: str

class ProjectDetailsRes(BaseModel):
    model_response: str
    inference_time: str
