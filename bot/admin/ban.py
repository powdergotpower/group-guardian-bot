"""
Ban command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter, can_restrict_filter
from bot.utils.parser import extract_user, get_mention


@Client.on_message(filters.command("ban") & filters.group & admin_filter & can_restrict_filter)
async def ban_user(client: Client, message: Message):
    """Ban a user from the group"""
    user_id, reason = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please reply to a user or provide a user ID/username.")
        return
    
    # Check if trying to ban self
    if user_id == message.from_user.id:
        await message.reply("❌ You can't ban yourself!")
        return
    
    # Check if trying to ban bot
    bot = await client.get_me()
    if user_id == bot.id:
        await message.reply("❌ I can't ban myself!")
        return
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Ban the user
        await client.ban_chat_member(message.chat.id, user_id)
        
        reason_text = f"\n📝 Reason: {reason}" if reason else ""
        await message.reply(
            f"🔨 **User Banned**\n"
            f"👤 User: {mention}\n"
            f"🆔 ID: `{user_id}`{reason_text}"
        )
        
    except Exception as e:
        await message.reply(f"❌ Failed to ban user: {str(e)}")


@Client.on_message(filters.command("unban") & filters.group & admin_filter & can_restrict_filter)
async def unban_user(client: Client, message: Message):
    """Unban a user from the group"""
    user_id, _ = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please provide a user ID/username to unban.")
        return
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Unban the user
        await client.unban_chat_member(message.chat.id, user_id)
        
        await message.reply(
            f"✅ **User Unbanned**\n"
            f"👤 User: {mention}\n"
            f"🆔 ID: `{user_id}`"
        )
        
    except Exception as e:
        await message.reply(f"❌ Failed to unban user: {str(e)}")
