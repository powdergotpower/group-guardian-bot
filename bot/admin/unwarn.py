"""
Unwarn command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter
from bot.utils.parser import extract_user, get_mention
from bot.database import db
from bot.config import WARN_LIMIT


@Client.on_message(filters.command("unwarn") & filters.group & admin_filter)
async def unwarn_user(client: Client, message: Message):
    """Remove a warn from a user"""
    user_id, _ = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please reply to a user or provide a user ID/username.")
        return
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Remove warn from database
        removed = await db.remove_warn(user_id, message.chat.id)
        
        if removed:
            warn_count = await db.get_warn_count(user_id, message.chat.id)
            await message.reply(
                f"✅ **Warn Removed**\n"
                f"👤 User: {mention}\n"
                f"🆔 ID: `{user_id}`\n"
                f"📊 Remaining warns: {warn_count}/{WARN_LIMIT}"
            )
        else:
            await message.reply(f"ℹ️ {mention} has no warnings to remove.")
        
    except Exception as e:
        await message.reply(f"❌ Failed to remove warn: {str(e)}")


@Client.on_message(filters.command("resetwarns") & filters.group & admin_filter)
async def reset_warns(client: Client, message: Message):
    """Reset all warns for a user"""
    user_id, _ = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please reply to a user or provide a user ID/username.")
        return
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Clear all warns
        await db.clear_warns(user_id, message.chat.id)
        
        await message.reply(
            f"✅ **Warns Reset**\n"
            f"👤 User: {mention}\n"
            f"🆔 ID: `{user_id}`\n"
            f"📊 All warnings have been cleared."
        )
        
    except Exception as e:
        await message.reply(f"❌ Failed to reset warns: {str(e)}")
