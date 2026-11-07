# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
# import os


# SESSION_FILE = "linkedin_session.json"


# def scrape_linkedin_job(job_url: str) -> dict:
#     """
#     Scrapes LinkedIn job page using a saved session.
#     Returns:
#         {
#             "title": str,
#             "company": str,
#             "description": str
#         }
#     """

#     if not os.path.exists(SESSION_FILE):
#         raise FileNotFoundError(
#             "linkedin_session.json not found. "
#             "Run save_session.py first to create it."
#         )

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state=SESSION_FILE)
#         page = context.new_page()

#         print("Opening job page...")
#         page.goto(job_url)
#         page.wait_for_timeout(5000)

#         try:
#             # Title
#             title = page.locator("h1").first.inner_text()

#             # Company name
#             company = page.locator(
#                 ".job-details-jobs-unified-top-card__company-name"
#             ).first.inner_text()

#             # Job description
#             description = page.locator(
#                 ".jobs-description-content__text"
#             ).first.inner_text()

#             print("Scraping successful!")
#             print("Title:", title)
#             print("Company:", company)

#         except PlaywrightTimeoutError:
#             print("Failed to load job details.")
#             browser.close()
#             return {}

#         browser.close()

#         return {
#             "title": title.strip(),
#             "company": company.strip(),
#             "description": description.strip()
#         }


# # 🔹 Test directly
# if __name__ == "__main__":
#     test_url = "https://www.linkedin.com/jobs/view/4308024473/"
#     job_data = scrape_linkedin_job(test_url)

#     print("\nFinal Result:")
#     print(job_data)


import os
import json
from playwright.sync_api import sync_playwright

SESSION_FILE = "linkedin_session.json"


def scrape_linkedin_job(job_url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # ✅ Load saved login session
        if os.path.exists(SESSION_FILE):
            context = browser.new_context(storage_state=SESSION_FILE)
        else:
            print("❌ No saved session found. Run save_session.py first.")
            return {}

        page = context.new_page()

        print("🚀 Opening LinkedIn job page...")
        page.goto(job_url)
        page.wait_for_timeout(5000)

        # -------- TITLE --------
        try:
            title = page.locator("h1").first.inner_text().strip()
        except:
            title = "Title Not Found"

        # -------- COMPANY --------
        try:
            company = page.locator("a[href*='/company/']").first.inner_text().strip()
        except:
            company = "Company Not Found"

        # -------- DESCRIPTION --------
        try:
            page.locator("button:has-text('Show more')").click(timeout=3000)
        except:
            pass

        try:
            description = page.locator("div.jobs-description-content").inner_text().strip()
        except:
            description = "Description Not Found"

        browser.close()

        print("✅ Scraping finished")
        print("TITLE:", title)
        print("COMPANY:", company)
        print("DESCRIPTION LENGTH:", len(description))

        return {
            "title": title,
            "company": company,
            "description": description,
        }


# 🔥 Run directly for testing
if __name__ == "__main__":
    test_url = "https://www.linkedin.com/jobs/view/4308024473/"
    result = scrape_linkedin_job(test_url)

    print("\n📦 Final Result:")
    print(result)
