"""
Unmute command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from bot.filters.admin_filter import admin_filter, can_restrict_filter
from bot.utils.parser import extract_user, get_mention


@Client.on_message(filters.command("unmute") & filters.group & admin_filter & can_restrict_filter)
async def unmute_user(client: Client, message: Message):
    """Unmute a user in the group"""
    user_id, _ = await extract_user(client, message)
    
    if not user_id:
        await message.reply("❌ Please reply to a user or provide a user ID/username.")
        return
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Get default chat permissions
        chat = await client.get_chat(message.chat.id)
        default_permissions = chat.permissions or ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_invite_users=True
        )
        
        # Unmute the user (restore permissions)
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            default_permissions
        )
        
        await message.reply(
            f"🔊 **User Unmuted**\n"
            f"👤 User: {mention}\n"
            f"🆔 ID: `{user_id}`"
        )
        
    except Exception as e:
        await message.reply(f"❌ Failed to unmute user: {str(e)}")
