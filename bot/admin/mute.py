"""
Mute command handler
"""
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from bot.filters.admin_filter import admin_filter, can_restrict_filter
from bot.utils.parser import extract_user, extract_time, get_mention, format_time


@Client.on_message(filters.command("mute") & filters.group & admin_filter & can_restrict_filter)
async def mute_user(client: Client, message: Message):
    """Mute a user in the group"""
    user_id, reason = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please reply to a user or provide a user ID/username.")
        return
    
    # Check if trying to mute self
    if user_id == message.from_user.id:
        await message.reply("❌ You can't mute yourself!")
        return
    
    # Check if trying to mute bot
    bot = await client.get_me()
    if user_id == bot.id:
        await message.reply("❌ I can't mute myself!")
        return
    
    # Check for time duration
    until_date = None
    time_text = ""
    
    if reason:
        seconds, remaining_reason = await extract_time(reason)
        if seconds:
            until_date = datetime.now() + timedelta(seconds=seconds)
            time_text = f"\n⏱ Duration: {format_time(seconds)}"
            reason = remaining_reason
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Mute the user (restrict all permissions)
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            ChatPermissions(),  # Empty permissions = muted
            until_date=until_date
        )
        
        reason_text = f"\n📝 Reason: {reason}" if reason else ""
        await message.reply(
            f"🔇 **User Muted**\n"
            f"👤 User: {mention}\n"
            f"🆔 ID: `{user_id}`{time_text}{reason_text}"
        )
        
    except Exception as e:
        await message.reply(f"❌ Failed to mute user: {str(e)}")
