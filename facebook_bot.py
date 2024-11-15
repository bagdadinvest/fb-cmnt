import asyncio
from playwright.async_api import async_playwright
import json
import random
import sys

# Load cookies from JSON file
async def load_cookies_from_file(filename):
    with open(filename, 'r') as f:
        cookies = json.load(f)
        for cookie in cookies:
            if 'sameSite' not in cookie or cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                cookie['sameSite'] = 'Lax'
        return cookies

async def random_scroll(page):
    """Random scrolling behavior to simulate human activity."""
    while True:
        await asyncio.sleep(random.randint(10, 30))  # Wait for a random interval
        for _ in range(random.randint(2, 5)):  # Random number of scrolls
            scroll_amount = random.randint(300, 700)
            await page.mouse.wheel(0, scroll_amount)
            print(f"Debug: Scrolled {scroll_amount} pixels down on main page.")
            await asyncio.sleep(random.uniform(0.5, 1.5))

async def handle_url(page, url):
    """Detect URL type and perform the necessary actions."""
    await page.goto(url)
    await page.wait_for_load_state()

    if "profile.php" in url:
        print("Detected a profile. Attempting to Add Friend.")
        add_friend_button = page.locator('div[aria-label="Add friend"]').first
        if await add_friend_button.is_visible():
            await add_friend_button.click()
            print("Debug: Sent friend request.")
        else:
            print("Debug: Add Friend button not found or already sent.")

    elif "posts" in url or "photo" in url or "share" in url:
        print("Detected a post. Performing Like, Comment, and Share.")

        # Like
        like_button = page.locator('div[aria-label="Like"]').first
        await like_button.click()
        print("Debug: Liked the post.")
        await asyncio.sleep(random.randint(3, 8))  # Random wait after Like

        # Comment
        comment_box = page.locator('div[aria-label^="Comment as"]').first
        await comment_box.fill("Nice post! 😊")
        send_button = page.locator('div[aria-label="Comment"]').first
        await send_button.click()
        print("Debug: Commented on the post.")
        await asyncio.sleep(random.randint(5, 10))  # Random wait after Comment

        # Share
        share_button = page.locator('div[aria-label^="Send this to friends"]').first
        await share_button.click()
        await asyncio.sleep(2)  # Wait for the share modal to appear
        share_now_button = page.locator('div[aria-label="Share now"]').first
        await share_now_button.click()
        print("Debug: Shared the post.")

    else:
        print("Detected a group. Attempting to Follow.")
        follow_button = page.locator('div[aria-label="Follow"]').first
        if await follow_button.is_visible():
            await follow_button.click()
            print("Debug: Followed the group.")
        else:
            print("Debug: Follow button not found. Attempting to Like the group.")
            like_button = page.locator('div[aria-label="Like"]').first
            if await like_button.is_visible():
                await like_button.click()
                print("Debug: Liked the group.")
            else:
                print("Debug: Like button also not found.")



    await asyncio.sleep(1)  # Simulate action delay

    # Return to Facebook main page after completing the action
    print("Returning to main page...")
    await page.goto("https://www.facebook.com")
    await page.wait_for_load_state()

async def async_input(prompt):
    """Asynchronously handle user input."""
    print(prompt, end="", flush=True)
    return await asyncio.to_thread(sys.stdin.readline)

async def listen_for_input(page):
    """Listen for URLs from the console asynchronously."""
    while True:
        url = (await async_input("Enter a Facebook URL: ")).strip()
        if url:
            try:
                await handle_url(page, url)
            except Exception as e:
                print(f"Error handling URL: {e}")
            print("Returning to idle state...")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Load cookies
        cookies = await load_cookies_from_file("cookies.json")
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto("https://www.facebook.com")
        print("Facebook loaded. Entering idle mode...")

        # Run random scrolling and user input in parallel
        await asyncio.gather(
            random_scroll(page),
            listen_for_input(page)
        )

if __name__ == "__main__":
    asyncio.run(main())
