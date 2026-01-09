#!/usr/bin/env python3
"""
Quick test for cover letter generator — STRICT quality checks.
This test FAILS if output is generic, placeholder, or low-quality.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("Health check passed")
            return True
        else:
            print(f"Health check failed: {response.text}")
            return False

    except Exception as e:
        print(f"Health error: {str(e)}")
        return False


def test_basic_functionality():
    """Test cover letter generation with STRICT validation."""
    print("  Test: Cover Letter Generation")
    print("=" * 60)

    test_data = {
    "resume_analysis": {
        "skills": [
            "Python",
            "FastAPI",
            "Django",
            "PostgreSQL",
            "Redis",
            "Docker",
            "REST APIs",
            "AWS",
            "Git"
        ],
        "projects": [
            {
                "name": "REST API Service",
                "description": (
                    "Designed and developed a RESTful API service for user management, "
                    "authentication, and role-based access control"
                ),
                "technologies": [
                    "Python", "FastAPI", "PostgreSQL", "JWT", "Docker"
                ]
            },
            {
                "name": "Task Queue System",
                "description": (
                    "Implemented an asynchronous task processing system to handle "
                    "background jobs and scheduled tasks"
                ),
                "technologies": [
                    "Python", "Redis", "Celery", "Docker"
                ]
            }
        ],
        "experience": [
            {
                "company": "CloudStack Solutions",
                "role": "Backend Developer",
                "duration": "3 years",
                "description": (
                    "Built and maintained backend services, optimized database queries, "
                    "and collaborated with frontend teams on API design"
                )
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Technology in Computer Science",
                "institution": "National Institute of Technology",
                "year": "2019"
            }
        ],
        "ats_score": 82
    },
    "job_info": {
        "company_name": "DataScale Systems",
        "job_title": "Backend Engineer",
        "job_description": (
            "We are looking for a Backend Engineer with strong experience in Python, "
            "REST API development, and database systems. The role involves building "
            "scalable backend services, improving system performance, and working "
            "closely with cross-functional teams."
        ),
        "tone": "confident"
    },
    "candidate_name": "John Doe"
}


    try:
        print(" Sending request...")
        response = requests.post(
            f"{BASE_URL}/cover-letter/generate-cover-letter",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        print(f" Status Code: {response.status_code}")

        if response.status_code != 200:
            print("FAIL: Non-200 response")
            print(response.text)
            return False

        result = response.json()
        cover_letter = result.get("cover_letter", {})

        greeting = cover_letter.get("greeting", "")
        body = cover_letter.get("body", [])
        closing = cover_letter.get("closing", "")
        sign_off = cover_letter.get("sign_off", "")
        candidate_name = cover_letter.get("candidate_name", "")

        print("\n🔧 ACTUAL JSON RESPONSE:")
        print("-" * 40)
        print(json.dumps(result, indent=2))
        print("-" * 40)

        # ---------------- STRICT QUALITY CHECKS ----------------

        full_text = " ".join(body).lower()

        #    1. Reject placeholders / garbage
        bad_markers = [
            "generated cover letter content",
            "paragraph 1",
            "placeholder",
            "lorem ipsum"
        ]

        for marker in bad_markers:
            if marker in full_text:
                print("  FAIL: Placeholder or generic content detected")
                return False

        #    2. Require at least 4 paragraphs
        if len(body) < 4:
            print(f"  FAIL: Expected ≥4 paragraphs, got {len(body)}")
            return False

        #    3. Ensure job title appears
        if "backend engineer" not in full_text:
            print("  FAIL: Job title not referenced in body")
            return False

        #    4. Ensure resume skills are actually used
        expected_skills = ["python", "fastapi", "postgresql"]
        missing_skills = [s for s in expected_skills if s not in full_text]

        if missing_skills:
            print(f"  FAIL: Missing expected skills: {missing_skills}")
            return False

        #    5. Greeting must include company
        if "datascale systems" not in greeting.lower():
            print("  FAIL: Company name missing in greeting")
            return False

        print(" Content quality checks PASSED")
        print(" TEST PASSED — Output is meaningful and role-aligned")
        return True

    except Exception as e:
        print(f" ERROR during test: {str(e)}")
        return False


if __name__ == "__main__":
    print(" Starting Test")
    print("Server must be running: python simple_server.py\n")

    if not test_health():
        print("  Health check failed — aborting")
    else:
        print()
        test_basic_functionality()
