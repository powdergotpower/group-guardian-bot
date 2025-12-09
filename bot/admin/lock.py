"""
Lock command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter, can_restrict_filter
from bot.database import db
from bot.config import LOCKABLE_TYPES


@Client.on_message(filters.command("lock") & filters.group & admin_filter & can_restrict_filter)
async def lock_type(client: Client, message: Message):
    """Lock a specific type of content"""
    if len(message.command) < 2:
        types_list = ", ".join(LOCKABLE_TYPES)
        await message.reply(
            f"❌ Please specify what to lock.\n"
            f"Available types: `{types_list}`\n"
            f"Usage: `/lock <type>`"
        )
        return
    
    lock_type = message.command[1].lower()
    
    if lock_type not in LOCKABLE_TYPES:
        types_list = ", ".join(LOCKABLE_TYPES)
        await message.reply(f"❌ Invalid type. Available: `{types_list}`")
        return
    
    try:
        # Add lock to database
        await db.add_lock(message.chat.id, lock_type)
        await message.reply(f"🔒 Locked: **{lock_type}**")
        
    except Exception as e:
        await message.reply(f"❌ Failed to lock: {str(e)}")


@Client.on_message(filters.command("locks") & filters.group)
async def list_locks(client: Client, message: Message):
    """List all locks in the chat"""
    try:
        locks = await db.get_locks(message.chat.id)
        
        if not locks:
            await message.reply("✅ No locks are active in this chat.")
            return
        
        locks_list = "\n".join([f"• {lock}" for lock in locks])
        await message.reply(f"🔒 **Active Locks:**\n{locks_list}")
        
    except Exception as e:
        await message.reply(f"❌ Failed to get locks: {str(e)}")
