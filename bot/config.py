"""
Configuration file for the bot
Load environment variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Required environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Bot settings
WARN_LIMIT = 3  # Number of warns before auto-ban
DEFAULT_WELCOME = "Welcome to the group, {mention}!"
DEFAULT_GOODBYE = "Goodbye, {name}!"

# Lockable types
LOCKABLE_TYPES = [
    "media", "photo", "video", "audio", "voice",
    "document", "sticker", "gif", "link", "forward"
]
