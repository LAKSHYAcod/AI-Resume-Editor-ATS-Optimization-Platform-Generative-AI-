import requests

API_URL = "http://127.0.0.1:8000/apply-with-ai"

payload = {
    "job_url": "https://www.linkedin.com/jobs/view/123456789/",
    "job_description": "Looking for a Python developer with FastAPI experience",
    "profile": {
        "name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "FastAPI", "SQL"],
        "experience": "3 years backend development"
    }
}

response = requests.post(API_URL, json=payload)
print(response.json())
