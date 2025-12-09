"""
Warn command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter, can_restrict_filter
from bot.utils.parser import extract_user, get_mention
from bot.database import db
from bot.config import WARN_LIMIT


@Client.on_message(filters.command("warn") & filters.group & admin_filter)
async def warn_user(client: Client, message: Message):
    """Warn a user"""
    user_id, reason = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please reply to a user or provide a user ID/username.")
        return
    
    # Check if trying to warn self
    if user_id == message.from_user.id:
        await message.reply("❌ You can't warn yourself!")
        return
    
    # Check if trying to warn bot
    bot = await client.get_me()
    if user_id == bot.id:
        await message.reply("❌ You can't warn me!")
        return
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Add warn to database
        warn_count = await db.add_warn(
            user_id=user_id,
            chat_id=message.chat.id,
            reason=reason or "No reason provided",
            warned_by=message.from_user.id
        )
        
        reason_text = f"\n📝 Reason: {reason}" if reason else ""
        
        # Check if user should be banned
        if warn_count >= WARN_LIMIT:
            await client.ban_chat_member(message.chat.id, user_id)
            await db.clear_warns(user_id, message.chat.id)
            
            await message.reply(
                f"🔨 **User Banned**\n"
                f"👤 User: {mention}\n"
                f"🆔 ID: `{user_id}`\n"
                f"⚠️ Reached {WARN_LIMIT} warnings!"
            )
        else:
            await message.reply(
                f"⚠️ **User Warned**\n"
                f"👤 User: {mention}\n"
                f"🆔 ID: `{user_id}`\n"
                f"📊 Warns: {warn_count}/{WARN_LIMIT}{reason_text}"
            )
        
    except Exception as e:
        await message.reply(f"❌ Failed to warn user: {str(e)}")
