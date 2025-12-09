"""
Unlock command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter, can_restrict_filter
from bot.database import db
from bot.config import LOCKABLE_TYPES


@Client.on_message(filters.command("unlock") & filters.group & admin_filter & can_restrict_filter)
async def unlock_type(client: Client, message: Message):
    """Unlock a specific type of content"""
    if len(message.command) < 2:
        types_list = ", ".join(LOCKABLE_TYPES)
        await message.reply(
            f"❌ Please specify what to unlock.\n"
            f"Available types: `{types_list}`\n"
            f"Usage: `/unlock <type>`"
        )
        return
    
    lock_type = message.command[1].lower()
    
    if lock_type == "all":
        # Unlock all types
        for lt in LOCKABLE_TYPES:
            await db.remove_lock(message.chat.id, lt)
        await message.reply("🔓 All locks removed!")
        return
    
    if lock_type not in LOCKABLE_TYPES:
        types_list = ", ".join(LOCKABLE_TYPES)
        await message.reply(f"❌ Invalid type. Available: `{types_list}`")
        return
    
    try:
        # Remove lock from database
        await db.remove_lock(message.chat.id, lock_type)
        await message.reply(f"🔓 Unlocked: **{lock_type}**")
        
    except Exception as e:
        await message.reply(f"❌ Failed to unlock: {str(e)}")
