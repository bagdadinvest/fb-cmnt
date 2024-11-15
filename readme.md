# Facebook Interaction Bot

## Overview
This script is a Facebook interaction bot built using Playwright. It simulates human activity by navigating through Facebook, adding friends, liking posts, sharing content, and more. It also provides the ability to manually handle URLs through the console.

## Features
- Loads cookies from a file to maintain a logged-in session.
- Simulates human-like scrolling behavior to avoid being detected as a bot.
- Asynchronously listens for Facebook URLs to perform certain actions such as adding friends, liking posts, commenting, and following groups.

## Requirements
- Python 3.8 or later
- Playwright (async version)
- JSON file containing Facebook cookies (`cookies.json`)

## Installation and Setup

1. **Clone the Repository**

   ```sh
   git clone <repository_link>
   cd facebook-interaction-bot
   ```

2. **Install Dependencies**

   Ensure you have Python 3.8 or newer installed. Then install the necessary Python libraries:

   ```sh
   pip install playwright
   playwright install
   ```

3. **Configure Cookies File**

   Create a `cookies.json` file and populate it with cookies in JSON format to keep your session active. The structure of the `cookies.json` should match what Playwright expects.

4. **Running the Bot**

   Run the bot script using the following command:

   ```sh
   python facebook_bot.py
   ```

## Script Usage
- Once started, the script will open Facebook and begin scrolling randomly to simulate human activity.
- You can enter Facebook URLs via the console to interact with specific posts, profiles, or groups.
  - **Profile**: The bot will attempt to add the user as a friend.
  - **Post**: The bot will like, comment, and share the post.
  - **Group**: The bot will try to follow or like the group.

## Code Explanation

- **Load Cookies**: Loads cookies from a JSON file to maintain your Facebook login session.
- **Random Scrolling**: The bot randomly scrolls to simulate human behavior and reduce the likelihood of detection.
- **Handle URL**: This function interacts with various Facebook elements based on the URL type:
  - **Profile.php** URL is identified as a user profile and triggers the "Add Friend" action.
  - URLs containing "posts", "photo", or "share" are treated as posts to like, comment, and share.
  - Other URLs are interpreted as group links, and actions like "Follow" or "Like" are attempted.
- **Async Input**: Captures user input from the console while the bot runs, allowing dynamic interactions.

## Safety Disclaimer
This script is meant for educational purposes only. Automating interactions on Facebook may violate their terms of service. Please use responsibly and at your own risk.

## Potential Issues
- **Captcha Detection**: Facebook may require additional verification due to bot-like activities.
- **Account Ban**: Using scripts like this can result in account suspension.


