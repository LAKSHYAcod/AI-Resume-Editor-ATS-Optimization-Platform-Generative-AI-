from playwright.sync_api import sync_playwright

def save_linkedin_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.linkedin.com/login")

        print("Login manually in the browser...")
        input("Press ENTER after you are logged in...")

        context.storage_state(path="linkedin_session.json")
        print("Session saved!")

        browser.close()

if __name__ == "__main__":
    save_linkedin_session()
