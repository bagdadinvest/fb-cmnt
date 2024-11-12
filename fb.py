from playwright.sync_api import sync_playwright
import json

# Load cookies from JSON file
def load_cookies_from_file(filename):
    with open(filename, 'r') as f:
        cookies = json.load(f)
        for cookie in cookies:
            if 'sameSite' not in cookie or cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                cookie['sameSite'] = 'Lax'  # Default to 'Lax'
        return cookies


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Load cookies
        cookies = load_cookies_from_file("cookies.json")
        context.add_cookies(cookies)

        page = context.new_page()
        page.goto("https://www.facebook.com")

        # Wait for the "What's on your mind" indicator
        page.wait_for_selector('span:has-text("What\'s on your mind, Lotfi?")', timeout=30000)

        # Now search for the first post
        page.wait_for_selector('div[aria-label="Leave a comment"]', timeout=30000)
        comment_button = page.locator('div[aria-label="Leave a comment"]').first
        comment_button.click()

        # Wait for the comment modal
        page.wait_for_selector('div[aria-label^="Comment as"]')

        # Type a comment
        comment_box = page.locator('div[aria-label^="Comment as"]').first
        comment_box.fill("Automated comment from Playwright!")

        # Click send
        send_button = page.locator('div[aria-label="Comment"]').first
        send_button.click()

        print("Comment posted successfully.")

        # Keep the browser open
        page.wait_for_timeout(3600000)

if __name__ == "__main__":
    main()
