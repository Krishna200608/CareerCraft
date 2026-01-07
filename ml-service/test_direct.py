import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("Testing health endpoint...")
response = client.get("/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\nTesting job-match endpoint...")
payload = {
    "resume_analysis": {
        "skills": ["python", "fastapi", "docker"],
        "ats_score": 74
    },
    "job_description": "Backend Engineer\nRequired: Python, FastAPI, AWS, Docker"
}

response = client.post("/resume/job-match", json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
