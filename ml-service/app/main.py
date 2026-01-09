from fastapi import FastAPI
from app.api import resume,health,cover_letter

app = FastAPI(title = "CareerCraft ML Service")

app.include_router(health.router, prefix="/health", tags=["System"])
app.include_router(resume.router, prefix="/resume", tags=["Extraction"])
app.include_router(cover_letter.router, prefix="/cover-letter", tags=["Cover Letter"])

@app.get("/")
async def root():
    return {"message": "ML Service is running"}