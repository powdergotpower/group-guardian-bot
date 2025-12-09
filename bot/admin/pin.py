"""
Pin command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter


@Client.on_message(filters.command("pin") & filters.group & admin_filter)
async def pin_message(client: Client, message: Message):
    """Pin a message"""
    if not message.reply_to_message:
        await message.reply("❌ Please reply to a message to pin it.")
        return
    
    # Check for silent pin
    silent = False
    if len(message.command) > 1:
        if message.command[1].lower() in ["silent", "quiet", "notify=false"]:
            silent = True
    
    try:
        await client.pin_chat_message(
            message.chat.id,
            message.reply_to_message.id,
            disable_notification=silent
        )
        
        mode = "silently " if silent else ""
        await message.reply(f"📌 Message {mode}pinned!")
        
    except Exception as e:
        await message.reply(f"❌ Failed to pin message: {str(e)}")
