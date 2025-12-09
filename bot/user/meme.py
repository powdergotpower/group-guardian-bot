"""
Meme command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.helpers import fetch_json


@Client.on_message(filters.command("meme"))
async def get_meme(client: Client, message: Message):
    """Get a random meme from Reddit"""
    await message.reply("🔄 Fetching a fresh meme...")
    
    try:
        # Use meme API
        data = await fetch_json("https://meme-api.com/gimme")
        
        if not data or "url" not in data:
            await message.reply("❌ Failed to fetch meme. Try again!")
            return
        
        caption = f"😂 **{data.get('title', 'Meme')}**\n"
        caption += f"👍 {data.get('ups', 0)} upvotes\n"
        caption += f"📍 r/{data.get('subreddit', 'memes')}"
        
        # Check if it's a video or image
        url = data["url"]
        if url.endswith((".gif", ".gifv")):
            await message.reply_animation(url, caption=caption)
        else:
            await message.reply_photo(url, caption=caption)
        
    except Exception as e:
        await message.reply(f"❌ Error fetching meme: {str(e)}")


@Client.on_message(filters.command("dankmeme"))
async def get_dank_meme(client: Client, message: Message):
    """Get a dank meme"""
    try:
        data = await fetch_json("https://meme-api.com/gimme/dankmemes")
        
        if not data or "url" not in data:
            await message.reply("❌ Failed to fetch dank meme.")
            return
        
        caption = f"🔥 **{data.get('title', 'Dank Meme')}**\n"
        caption += f"👍 {data.get('ups', 0)} | r/{data.get('subreddit', 'dankmemes')}"
        
        await message.reply_photo(data["url"], caption=caption)
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
