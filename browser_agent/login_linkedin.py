# from playwright.sync_api import sync_playwright

# def login_and_save_state():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         page.goto("https://www.linkedin.com/login")

#         print("🔐 Please log in manually...")
#         page.wait_for_url("**/feed", timeout=0)

#         context.storage_state(path="linkedin_state.json")
#         print("✅ Login saved to linkedin_state.json")

#         browser.close()

# if __name__ == "__main__":
#     login_and_save_state()
def test_login():
    from playwright.sync_api import sync_playwright
    import os

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.linkedin.com/login")

        page.fill("#username", os.getenv("LINKEDIN_EMAIL"))
        page.fill("#password", os.getenv("LINKEDIN_PASSWORD"))
        page.click("button[type=submit]")

        page.wait_for_timeout(10000)

        print("Check if login worked manually.")

        browser.close()
