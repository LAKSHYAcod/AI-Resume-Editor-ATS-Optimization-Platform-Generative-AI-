# # from playwright.sync_api import sync_playwright, TimeoutError
# # import os
# # import time

# # def auto_apply(job_url: str, name: str, email: str, resume_path: str | None = None):
# #     with sync_playwright() as p:
# #         browser = p.chromium.launch(headless=False)

# #         context = browser.new_context(
# #             storage_state="linkedin_state.json" if os.path.exists("linkedin_state.json") else None
# #         )
# #         page = context.new_page()

# #         # 1. Open job page
# #         page.goto(job_url, timeout=60000)

# #         # 2. Click Easy Apply if exists
# #         try:
# #             page.get_by_role("button", name="Easy Apply").click(timeout=10000)
# #         except TimeoutError:
# #             print("❌ Easy Apply not available for this job")
# #             return

# #         time.sleep(2)

# #         # 3. Fill email if needed
# #         email_input = page.locator("input[type='email']")
# #         if email_input.count() > 0:
# #             email_input.first.fill(email)

# #         # 4. Upload resume
# #         if resume_path:
# #             file_input = page.locator("input[type='file']")
# #             if file_input.count() > 0:
# #                 file_input.first.set_input_files(resume_path)

# #         print("✅ Form filled. Please review and submit manually.")
# #         input("➡️ Press ENTER after submitting...")

# #         browser.close()

# import json
# import time
# from playwright.sync_api import sync_playwright


# SESSION_FILE = "linkedin_session.json"


# def auto_apply(job_url: str, name: str, email: str):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)

#         # ✅ Load saved login session
#         context = browser.new_context(storage_state=SESSION_FILE)
#         page = context.new_page()

#         print("🚀 Opening job page...")
#         page.goto(job_url)
#         page.wait_for_timeout(4000)

#         # ✅ Click Easy Apply
#         try:
#             easy_apply_btn = page.locator("button:has-text('Easy Apply')")
#             easy_apply_btn.first.click()
#             print("✅ Easy Apply clicked")
#         except:
#             print("❌ Easy Apply button not found")
#             browser.close()
#             return

#         time.sleep(2)

#         # ✅ Fill Phone (if required)
#         try:
#             phone_input = page.locator("input[type='tel']")
#             if phone_input.count() > 0:
#                 phone_input.first.fill("9999999999")
#                 print("📞 Phone filled")
#         except:
#             pass

#         # ✅ Click Next / Review / Submit repeatedly
#         while True:
#             time.sleep(2)

#             if page.locator("button:has-text('Submit application')").count() > 0:
#                 page.locator("button:has-text('Submit application')").click()
#                 print("🎉 Application Submitted!")
#                 break

#             elif page.locator("button:has-text('Review')").count() > 0:
#                 page.locator("button:has-text('Review')").click()

#             elif page.locator("button:has-text('Next')").count() > 0:
#                 page.locator("button:has-text('Next')").click()

#             else:
#                 print("⚠️ Unknown step encountered")
#                 break

#         time.sleep(5)
#         browser.close()


# from playwright.sync_api import sync_playwright
# import time


# def auto_apply(job_url: str, name: str, email: str):
#     """
#     Automatically applies to a LinkedIn Easy Apply job.
#     """

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state="linkedin_session.json")
#         page = context.new_page()

#         print("🚀 Opening job page...")
#         page.goto(job_url)
#         page.wait_for_timeout(3000)

#         try:
#             # Click Easy Apply button
#             easy_apply_btn = page.get_by_role("button", name="Easy Apply")
#             easy_apply_btn.first.click()
#             page.wait_for_timeout(2000)

#             print("✅ Easy Apply clicked")

#             handle_application_steps(page)

#         except Exception as e:
#             print("❌ Error during auto apply:", e)

#         browser.close()


# def handle_application_steps(page):
#     """
#     Handles multi-step Easy Apply modal.
#     """

#     while True:
#         page.wait_for_timeout(1500)

#         # --- Fill basic fields if visible ---
#         fill_input_if_exists(page, "input[name='email']", "your@email.com")
#         fill_input_if_exists(page, "input[name='phoneNumber']", "9999999999")

#         # --- NEXT BUTTON ---
#         next_btn = page.get_by_role("button", name="Continue to next step")
#         if next_btn.count() > 0:
#             print("➡ Clicking Next")
#             next_btn.first.click()
#             continue

#         # --- REVIEW BUTTON ---
#         review_btn = page.get_by_role("button", name="Review your application")
#         if review_btn.count() > 0:
#             print("📝 Clicking Review")
#             review_btn.first.click()
#             continue

#         # --- SUBMIT BUTTON ---
#         submit_btn = page.get_by_role("button", name="Submit application")
#         if submit_btn.count() > 0:
#             print("🎯 Submitting application")
#             submit_btn.first.click()
#             page.wait_for_timeout(3000)
#             print("✅ Application Submitted Successfully!")
#             break

#         print("⚠ No more steps found")
#         break


# def fill_input_if_exists(page, selector: str, value: str):
#     """
#     Safely fills input if it exists.
#     """
#     element = page.locator(selector)

#     if element.count() > 0:
#         try:
#             element.first.fill(value)
#             print(f"✍ Filled field: {selector}")
#         except:
#             pass



# from playwright.sync_api import sync_playwright
# import time


# def auto_apply(job_url: str, name: str, email: str):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state="linkedin_session.json")
#         page = context.new_page()

#         print("🚀 Opening job page...")
#         page.goto(job_url)
#         page.wait_for_timeout(4000)

#         # Click Easy Apply
#         try:
#             page.get_by_role("button", name="Easy Apply").click()
#             print("✅ Easy Apply clicked")
#             page.wait_for_timeout(3000)
#         except:
#             print("❌ Easy Apply button not found")
#             browser.close()
#             return

#         handle_application_steps(page)

#         browser.close()


# def handle_application_steps(page):
#     max_steps = 15
#     step_count = 0

#     while step_count < max_steps:
#         step_count += 1
#         time.sleep(2)

#         # Submit button
#         if page.locator("button:has-text('Submit application')").count() > 0:
#             print("📤 Submitting application...")
#             page.locator("button:has-text('Submit application')").click()
#             print("✅ Application Submitted Successfully!")
#             break

#         # Review button
#         elif page.locator("button:has-text('Review')").count() > 0:
#             print("📝 Clicking Review")
#             page.locator("button:has-text('Review')").first.click()

#         # Next button
#         elif page.locator("button:has-text('Next')").count() > 0:
#             print("➡ Clicking Next")
#             page.locator("button:has-text('Next')").first.click()

#         else:
#             print("⚠ No more steps found")
#             break




# browser_agent/auto_apply.py

from playwright.sync_api import sync_playwright


def auto_apply(job_url: str, name: str, email: str, resume_path: str | None = None):
    """
    Automatically applies to a LinkedIn job using Easy Apply.
    """

    print("🚀 Starting Auto Apply...")
    print("Job URL:", job_url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="linkedin_session.json")
        page = context.new_page()

        # Open job page
        page.goto(job_url)
        page.wait_for_timeout(5000)

        # Click Easy Apply
        easy_apply_button = page.locator("button:has-text('Easy Apply')")

        if easy_apply_button.count() == 0:
            print("❌ Easy Apply button not found.")
            browser.close()
            return

        easy_apply_button.first.click()
        page.wait_for_timeout(3000)

        print("✅ Easy Apply clicked")

        # Handle application steps
        while True:
            next_button = page.locator("button:has-text('Next')")
            review_button = page.locator("button:has-text('Review')")
            submit_button = page.locator("button:has-text('Submit application')")

            if next_button.count() > 0:
                print("➡ Clicking Next")
                next_button.first.click()
                page.wait_for_timeout(20000)

            elif review_button.count() > 0:
                print("📝 Clicking Review")
                review_button.first.click()
                page.wait_for_timeout(20000)

            elif submit_button.count() > 0:
                print("📨 Submitting application")
                submit_button.first.click()
                page.wait_for_timeout(3000)
                print("🎉 Application Submitted Successfully!")
                break

            else:
                print("⚠ No more steps found.")
                break

        browser.close()




