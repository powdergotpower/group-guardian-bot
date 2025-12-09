"""
Slowmode command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter


@Client.on_message(filters.command("slowmode") & filters.group & admin_filter)
async def set_slowmode(client: Client, message: Message):
    """Set slowmode for the chat"""
    if len(message.command) < 2:
        await message.reply(
            "❌ Please specify slowmode duration.\n"
            "Usage: `/slowmode <seconds>`\n"
            "Use `/slowmode 0` or `/slowmode off` to disable."
        )
        return
    
    arg = message.command[1].lower()
    
    # Handle off/disable
    if arg in ["off", "disable", "0"]:
        seconds = 0
    else:
        try:
            seconds = int(arg)
        except ValueError:
            await message.reply("❌ Please provide a valid number of seconds.")
            return
    
    # Validate range (0-86400 seconds = 0-24 hours)
    if seconds < 0 or seconds > 86400:
        await message.reply("❌ Slowmode must be between 0 and 86400 seconds (24 hours).")
        return
    
    try:
        await client.set_chat_slow_mode_delay(message.chat.id, seconds)
        
        if seconds == 0:
            await message.reply("✅ Slowmode disabled.")
        else:
            await message.reply(f"✅ Slowmode set to {seconds} seconds.")
        
    except Exception as e:
        await message.reply(f"❌ Failed to set slowmode: {str(e)}")
