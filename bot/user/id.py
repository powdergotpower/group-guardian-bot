"""
ID command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("id"))
async def get_id(client: Client, message: Message):
    """Get user and chat IDs"""
    text = ""
    
    # Add chat info
    text += f"💬 **Chat ID:** `{message.chat.id}`\n"
    
    if message.chat.title:
        text += f"📝 **Chat Title:** {message.chat.title}\n"
    
    text += "\n"
    
    # Add user info
    if message.from_user:
        text += f"👤 **Your ID:** `{message.from_user.id}`\n"
        if message.from_user.username:
            text += f"📛 **Username:** @{message.from_user.username}\n"
    
    # Add replied user info
    if message.reply_to_message and message.reply_to_message.from_user:
        replied_user = message.reply_to_message.from_user
        text += f"\n👤 **Replied User ID:** `{replied_user.id}`\n"
        if replied_user.username:
            text += f"📛 **Username:** @{replied_user.username}\n"
        text += f"💬 **Message ID:** `{message.reply_to_message.id}`\n"
    
    # Add forwarded info
    if message.reply_to_message and message.reply_to_message.forward_from:
        forwarded = message.reply_to_message.forward_from
        text += f"\n↪️ **Forwarded From ID:** `{forwarded.id}`\n"
        if forwarded.username:
            text += f"📛 **Username:** @{forwarded.username}\n"
    
    if message.reply_to_message and message.reply_to_message.forward_from_chat:
        forwarded_chat = message.reply_to_message.forward_from_chat
        text += f"\n↪️ **Forwarded Chat ID:** `{forwarded_chat.id}`\n"
        if forwarded_chat.username:
            text += f"📛 **Username:** @{forwarded_chat.username}\n"
    
    await message.reply(text)
