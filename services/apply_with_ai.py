from ai.resume_generator import generate_resume
from utils.save_resume import save_resume
from browser_agent.job_scraper import scrape_linkedin_job


def apply_with_ai(profile, job_url: str, job_description: str = None):

    print("🔎 Scraping job from LinkedIn...")
    job_data = scrape_linkedin_job(job_url)

    if not job_data:
        return {"error": "Failed to scrape job data."}

    print("🧠 Generating tailored resume...")

    resume_text = generate_resume(
        profile=profile,
        job_title=job_data["title"],
        company=job_data["company"],
        job_description=job_data["description"],
    )

    save_resume(resume_text, "ai_resume.txt")

    return {
        "resume_text": resume_text,
        "job_title": job_data["title"],
        "company": job_data["company"],
    }
