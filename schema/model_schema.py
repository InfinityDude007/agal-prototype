from pydantic import BaseModel


class ProjectDetails(BaseModel):
    project_type: str
    project_goal: str
    company_industry: str
    investment: str
    countries: str


class GeneratedPrompt(BaseModel):
    prompt: str


class ModelResponse(BaseModel):
    response: set
    time_elapsed: float
