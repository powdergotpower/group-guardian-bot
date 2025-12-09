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
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
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
