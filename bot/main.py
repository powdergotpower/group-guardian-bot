"""
Telegram Group Management Bot
Main entry point
"""
import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from database import Database

# Initialize database
db = Database()

# Initialize bot
app = Client(
    "group_manager_bot",
    api_id=22071176,
    api_hash="7ed5401b625a0a4d3c45caf12c87f166",
    bot_token="7918136133:AAEdGPNoeRAtory8zUGKR8-dBU6GAJNQ5D8",
    plugins=dict(root="bot")
)


async def main():
    """Start the bot"""
    await db.init()
    await app.start()
    print("Bot started successfully!")
    print(f"Bot username: @{(await app.get_me()).username}")
    await idle()
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
