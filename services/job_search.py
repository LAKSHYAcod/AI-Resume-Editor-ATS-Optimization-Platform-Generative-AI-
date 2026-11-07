import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")


def search_job_from_interest(keyword: str):
    """
    Search jobs using Google Jobs via SerpAPI.
    Returns the first matching job.
    """

    if not SERP_API_KEY:
        print("SERP_API_KEY not found in .env")
        return None

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_jobs",
        "q": keyword,
        "location": "India",
        "hl": "en",
        "api_key": SERP_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        jobs = data.get("jobs_results", [])

        # If no jobs found, try fallback search
        if not jobs:
            print("No jobs found for:", keyword)
            print("Trying fallback search...")

            params["q"] = keyword.split()[0]  # shorter keyword
            response = requests.get(url, params=params)
            data = response.json()
            jobs = data.get("jobs_results", [])

        if not jobs:
            print("Still no jobs found.")
            return None

        first_job = jobs[0]

        job_title = first_job.get("title", "Unknown Title")
        company = first_job.get("company_name", "Unknown Company")
        location = first_job.get("location", "Unknown Location")
        description = first_job.get("description", "")

        apply_link = None
        related_links = first_job.get("related_links", [])

        if related_links:
            apply_link = related_links[0].get("link")

        job_data = {
            "title": job_title,
            "company": company,
            "location": location,
            "description": description,
            "apply_link": apply_link
        }

        print("Job Found:", job_title, "-", company)

        return job_data

    except Exception as e:
        print("Job search error:", str(e))
        return None