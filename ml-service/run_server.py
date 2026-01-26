"""
Simple server runner for testing the ML service.
Use this if uvicorn --reload has issues.
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting CareerCraft ML Service...")
    print("📍 URL: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
