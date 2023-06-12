import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Telegram bot token and chat ID from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

# Check if Telegram bot token and chat ID are available
if TOKEN is None or chat_id is None:
    print("Error: Please provide a valid TELEGRAM_BOT_TOKEN and CHAT_ID in the .env file.")
    exit(1)

# Read the message from previous_day_message.txt
try:
    with open("previous_day_message.txt", "r") as file:
        message = file.read()
except FileNotFoundError:
    print("Error: previous_day_message.txt file not found.")
    exit(1)

# Send the message using Telegram Bot API
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
params = {"chat_id": chat_id, "text": message}

try:
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
except requests.RequestException as e:
    print(f"Error: Failed to send message. {e}")
    exit(1)
