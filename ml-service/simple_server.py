#!/usr/bin/env python3
"""
Simple test server for cover letter generator.
This bypasses the existing services to test our new functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import only our cover letter functionality
from app.api.cover_letter import router as cover_letter_router
from app.api.health import router as health_router

app = FastAPI(title="CareerCraft ML Service - Cover Letter Test")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only working routes
app.include_router(health_router, prefix="/health", tags=["System"])
app.include_router(cover_letter_router, prefix="/cover-letter", tags=["Cover Letter"])

@app.get("/")
async def root():
    return {"message": "Cover Letter ML Service is running"}

if __name__ == "__main__":
    print("Starting Cover Letter Test Server...")
    print("Server will be available at: http://localhost:8000")
    print("Run tests with: python test_cover_letter.py")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
