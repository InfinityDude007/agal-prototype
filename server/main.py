import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from utils import get_local_timestamp
from dotenv import load_dotenv
import os
from routes import main_router

load_dotenv()



# --- FastAPI and CORS config ---

app = FastAPI(root_path="/api")
app.include_router(main_router)

origins = os.getenv("CORS_ORIGINS", "").split(",")
origins = [origin for origin in origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



# --- Root and health check endpoints ---

class RootResponse(BaseModel):
    message: str

@app.get("/", response_model=RootResponse, summary="Root endpoint", tags=["General"])
async def root():
    return RootResponse(
        message="Server hello"
    )


class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str

@app.get("/health", response_model=HealthResponse, summary="Check server health", tags=["Health"])
async def health_check():
    return HealthResponse(
        status="ok",
        message="Server is healthy",
        timestamp=get_local_timestamp()
    )



# --- ASGI config ---

class Settings(BaseSettings):
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", 8000))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.backend_host, port=settings.backend_port, reload=settings.debug)
