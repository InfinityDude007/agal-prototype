from pydantic import BaseModel

class GenericError(BaseModel):
    error: str
    status_code: int
    details: str
