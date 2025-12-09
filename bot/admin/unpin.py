"""
Unpin command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter


@Client.on_message(filters.command("unpin") & filters.group & admin_filter)
async def unpin_message(client: Client, message: Message):
    """Unpin a message or all messages"""
    # Check if unpinning all
    unpin_all = False
    if len(message.command) > 1:
        if message.command[1].lower() == "all":
            unpin_all = True
    
    try:
        if unpin_all:
            await client.unpin_all_chat_messages(message.chat.id)
            await message.reply("📌 All messages unpinned!")
        elif message.reply_to_message:
            await client.unpin_chat_message(message.chat.id, message.reply_to_message.id)
            await message.reply("📌 Message unpinned!")
        else:
            # Unpin the latest pinned message
            await client.unpin_chat_message(message.chat.id)
            await message.reply("📌 Latest pinned message unpinned!")
        
    except Exception as e:
        await message.reply(f"❌ Failed to unpin: {str(e)}")
