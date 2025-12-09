"""
Ping command handler
"""
import time
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("ping"))
async def ping(client: Client, message: Message):
    """Check bot latency"""
    start_time = time.time()
    
    msg = await message.reply("🏓 Pinging...")
    
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    
    await msg.edit_text(f"🏓 **Pong!**\n⏱ Latency: `{latency:.2f}ms`")
