"""
Test Script for Job-Resume Skill Matching Engine

This script tests the /resume/job-match endpoint with sample data.
Run this after starting the ML service to verify the implementation.
"""

import requests
import json

# ML Service endpoint
BASE_URL = "http://localhost:8001"
JOB_MATCH_URL = f"{BASE_URL}/resume/job-match"

# Sample resume analysis output (from /analyze endpoint)
SAMPLE_RESUME_ANALYSIS = {
    "skills": [
        "python",
        "fastapi",
        "mongodb",
        "react",
        "docker",
        "git",
        "javascript",
        "node.js",
        "sql"
    ],
    "ats_score": 74
}

# Sample job description
SAMPLE_JOB_DESCRIPTION = """
Software Engineer - Backend

Requirements:
- 3+ years of experience in backend development
- Strong proficiency in Python and FastAPI
- Experience with AWS cloud services
- Knowledge of Kubernetes and Docker
- Experience with PostgreSQL or MongoDB databases
- Understanding of microservices architecture
- Proficiency in Git version control

Technical Skills Required:
- Python, FastAPI, Flask, or Django
- AWS, EC2, S3, Lambda
- Kubernetes, Docker
- PostgreSQL, MongoDB
- RESTful API design
- CI/CD pipelines
- Unit testing and integration testing

Nice to have:
- Experience with React or Vue.js
- Knowledge of GraphQL
- Familiarity with Terraform
"""


def test_job_match():
    """Test the job-match endpoint"""
    
    print("=" * 80)
    print("Testing Job-Resume Skill Matching Engine")
    print("=" * 80)
    print()
    
    # Prepare request
    payload = {
        "resume_analysis": SAMPLE_RESUME_ANALYSIS,
        "job_description": SAMPLE_JOB_DESCRIPTION
    }
    
    print("📤 Sending request to:", JOB_MATCH_URL)
    print()
    print("📄 Resume Skills:", ", ".join(SAMPLE_RESUME_ANALYSIS["skills"]))
    print("📄 ATS Score:", SAMPLE_RESUME_ANALYSIS["ats_score"])
    print()
    
    try:
        # Make request
        response = requests.post(JOB_MATCH_URL, json=payload)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS! Job matching completed.")
            print()
            print("=" * 80)
            print("📊 RESULTS")
            print("=" * 80)
            print()
            print(f"🎯 Job Fit Score: {result['job_fit_score']}/100")
            print(f"📈 Skill Match Percentage: {result['skill_match_percentage']}%")
            print()
            
            print(f"✅ Matched Skills ({len(result['matched_skills'])}):")
            if result['matched_skills']:
                for skill in result['matched_skills']:
                    print(f"   • {skill}")
            else:
                print("   (none)")
            print()
            
            print(f"⚠️  Partial Matches ({len(result['partial_matches'])}):")
            if result['partial_matches']:
                for skill in result['partial_matches']:
                    print(f"   • {skill}")
            else:
                print("   (none)")
            print()
            
            print(f"❌ Missing Skills ({len(result['missing_skills'])}):")
            if result['missing_skills']:
                for skill in result['missing_skills']:
                    print(f"   • {skill}")
            else:
                print("   (none)")
            print()
            
            print("💡 Job Feedback:")
            for i, feedback in enumerate(result['job_feedback'], 1):
                print(f"   {i}. {feedback}")
            print()
            
            print("=" * 80)
            print("📋 Full JSON Response:")
            print("=" * 80)
            print(json.dumps(result, indent=2))
            
        else:
            print(f"❌ ERROR: Request failed with status code {response.status_code}")
            print("Response:", response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to ML service.")
        print("Make sure the service is running at", BASE_URL)
        print()
        print("To start the service, run:")
        print("  cd ml-service")
        print("  python -m uvicorn app.main:app --reload --port 8001")
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def test_health():
    """Test if the service is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ ML Service is healthy!")
            return True
        else:
            print("⚠️  ML Service returned non-200 status")
            return False
    except:
        print("❌ ML Service is not running")
        return False


if __name__ == "__main__":
    print()
    print("🧪 CareerCraft Job Matching Test")
    print()
    
    # Check health first
    if test_health():
        print()
        test_job_match()
    else:
        print()
        print("Please start the ML service first:")
        print("  cd ml-service")
        print("  python -m uvicorn app.main:app --reload --port 8001")
