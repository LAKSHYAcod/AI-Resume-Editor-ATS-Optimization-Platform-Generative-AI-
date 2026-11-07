from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
import re

# Existing imports
from browser_agent.auto_apply import auto_apply
from models.profile import UserProfile
from services.apply_with_ai import apply_with_ai
from utils.openrouter_client import generate_text

load_dotenv()

app = FastAPI()

# ==============================
# Middleware
# ==============================
@app.middleware("http")
async def disable_cache(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


app.mount("/static", StaticFiles(directory="static"), name="static")

# ==============================
# Basic Routes
# ==============================

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


# ==============================
# JOB SEARCH (SerpAPI)
# ==============================

SERP_API_KEY = os.getenv("SERP_API_KEY")

def search_job_from_interest(keyword: str):

    if not SERP_API_KEY:
        return None

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_jobs",
        "q": keyword,
        "hl": "en",
        "api_key": SERP_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        jobs = data.get("jobs_results", [])
        if not jobs:
            return None

        first_job = jobs[0]

        return {
            "title": first_job.get("title"),
            "company": first_job.get("company_name"),
            "location": first_job.get("location"),
            "description": first_job.get("description"),
            "apply_link": first_job.get("related_links", [{}])[0].get("link")
        }

    except Exception as e:
        print("Job search error:", e)
        return None


# ==============================
# ATS SYSTEM
# ==============================

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    return set(words)


def calculate_ats_score(resume_text, job_description):

    if not resume_text or not job_description:
        return 0

    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    if len(job_keywords) == 0:
        return 0

    matched = resume_keywords.intersection(job_keywords)
    score = (len(matched) / len(job_keywords)) * 100

    return round(score, 2)


# ==============================
# AUTO GENERATE
# ==============================
@app.post("/auto-generate")
async def auto_generate(data: dict):

    interest = data.get("interest")
    profile = data.get("profile")

    if not interest:
        return {"error": "Interest required"}

    # search job
    job = search_job_from_interest(interest)

    if not job:
        return {"error": "No jobs found"}

    job_description = job.get("description", "")

    name = profile.get("name", "")
    email = profile.get("email", "")
    linkedin = profile.get("linkedin", "")
    github = profile.get("github", "")
    experience = profile.get("experience", "")
    skills = profile.get("skills", [])

    skills_text = ", ".join(skills) if isinstance(skills, list) else skills
    prompt = f"""
    Generate a professional ATS optimized resume using the following format.
    {name}
    {email} | {linkedin} | {github}
    PROFESSIONAL SUMMARY
    SKILLS
    EXPERIENCE
    PROJECTS
    EDUCATION

    Candidate Details:
    Experience: {experience} years
    Skills: {skills_text}

    Match the following job description:
    {job_description}

    IMPORTANT:
    - Name and contact must appear at the very top
    - Do not repeat contact details at bottom
    - Use bullet points
    """

    

    resume_text = generate_text(prompt)

    ats_score = calculate_ats_score(resume_text, job_description)

    os.makedirs("generated_resumes", exist_ok=True)

    with open("generated_resumes/ai_resume.txt", "w", encoding="utf-8") as f:
        f.write(resume_text)
        return {
            "job_title": job["title"],
            "company": job["company"],
            "resume_text": resume_text,
            "ats_score": ats_score
            }


# ==============================
# EDIT RESUME
# ==============================

@app.post("/edit-resume")
async def edit_resume(data: dict):

    updated_resume = data.get("resume_text")
    job_description = data.get("job_description")

    if not updated_resume or not job_description:
        return {"error": "Resume and job description required"}

    ats_score = calculate_ats_score(updated_resume, job_description)

    with open("generated_resumes/ai_resume.txt", "w", encoding="utf-8") as f:
        f.write(updated_resume)

    return {
        "status": "updated",
        "resume_text": updated_resume,
        "ats_score": ats_score
    }


# ==============================
# EXISTING FEATURES
# ==============================

class AutoApplyRequest(BaseModel):
    job_url: str
    name: str
    email: str
    resume_path: str | None = None


class ApplyWithAIRequest(BaseModel):
    job_url: str
    job_description: str
    profile: UserProfile


@app.post("/auto-apply")
def auto_apply_endpoint(data: AutoApplyRequest):
    auto_apply(
        job_url=data.job_url,
        name=data.name,
        email=data.email,
        resume_path=data.resume_path
    )
    return {"status": "submitted"}


@app.post("/apply-with-ai")
def apply_with_ai_endpoint(data: ApplyWithAIRequest):
    resume_text = apply_with_ai(
        data.profile,
        data.job_url,
        data.job_description
    )

    return {
        "status": "success",
        "resume_text": resume_text
    }


@app.get("/download-resume")
async def download_resume():
    file_path = "generated_resumes/ai_resume.txt"

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="AI_Resume.txt",
            media_type="text/plain"
        )

    return {"error": "Resume not found"}