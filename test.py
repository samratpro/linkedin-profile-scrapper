from time import sleep
from playwright.sync_api import sync_playwright
import os
import json

# File to store cookies
storage_state_file = "storage_state.json"
def is_storage_state_valid(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                json.load(f)  # Attempt to load JSON to validate
                return True
            except json.JSONDecodeError:
                return False
    return False

# First run: Saving session and cookies
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False,args=['--disable-blink-features=AutomationControlled'])
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.linkedin.com/feed/")
    # Prompt the user to log in
    input("Please log in and then press Enter to close the browser...")
    # Save the storage state (including cookies)
    context.storage_state(path=storage_state_file)
    print("Session saved.")

    browser.close()

# Second run: Loading session and cookies
if is_storage_state_valid(storage_state_file):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
        )

        context = browser.new_context(storage_state=storage_state_file)
        page = context.new_page()
        page.goto("https://www.linkedin.com/")

        sleep(100)  # Wait to see the effect of the reused session

        browser.close()
else:
    print("Invalid or missing storage state file.")
