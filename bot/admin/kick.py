"""
Kick command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter, can_restrict_filter
from bot.utils.parser import extract_user, get_mention


@Client.on_message(filters.command("kick") & filters.group & admin_filter & can_restrict_filter)
async def kick_user(client: Client, message: Message):
    """Kick a user from the group (they can rejoin)"""
    user_id, reason = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please reply to a user or provide a user ID/username.")
        return
    
    # Check if trying to kick self
    if user_id == message.from_user.id:
        await message.reply("❌ You can't kick yourself!")
        return
    
    # Check if trying to kick bot
    bot = await client.get_me()
    if user_id == bot.id:
        await message.reply("❌ I can't kick myself!")
        return
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Kick the user (ban then unban)
        await client.ban_chat_member(message.chat.id, user_id)
        await client.unban_chat_member(message.chat.id, user_id)
        
        reason_text = f"\n📝 Reason: {reason}" if reason else ""
        await message.reply(
            f"👢 **User Kicked**\n"
            f"👤 User: {mention}\n"
            f"🆔 ID: `{user_id}`{reason_text}"
        )
        
    except Exception as e:
        await message.reply(f"❌ Failed to kick user: {str(e)}")
