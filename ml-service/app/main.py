import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import resume,health,cover_letter

app = FastAPI(title = "CareerCraft ML Service")

allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "").split(",") if os.getenv("CORS_ALLOW_ORIGINS") else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["System"])
app.include_router(resume.router, prefix="/resume", tags=["Extraction"])
app.include_router(cover_letter.router, prefix="/cover-letter", tags=["Cover Letter"])

@app.get("/")
async def root():
    return {"message": "ML Service is running"}