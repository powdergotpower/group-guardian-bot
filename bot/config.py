"""
Configuration file for the bot
Load environment variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Required environment variables
API_ID = int(os.getenv("22071176", "0"))
API_HASH = os.getenv("7ed5401b625a0a4d3c45caf12c87f166", "")
BOT_TOKEN = os.getenv("7918136133:AAEdGPNoeRAtory8zUGKR8-dBU6GAJNQ5D8", "")
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
