"""
Info command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from bot.utils.parser import extract_user, get_mention


@Client.on_message(filters.command("info"))
async def user_info(client: Client, message: Message):
    """Get detailed user information"""
    user_id, _ = await extract_user(client, message)
    
    # If no user specified, show own info
    if not user_id:
        user_id = message.from_user.id
    
    try:
        user = await client.get_users(user_id)
        
        # Build info text
        text = f"👤 **User Information**\n\n"
        text += f"**Name:** {user.first_name}"
        if user.last_name:
            text += f" {user.last_name}"
        text += "\n"
        
        text += f"**ID:** `{user.id}`\n"
        
        if user.username:
            text += f"**Username:** @{user.username}\n"
        
        text += f"**Mention:** {get_mention(user)}\n"
        
        # DC ID
        if user.dc_id:
            text += f"**DC ID:** {user.dc_id}\n"
        
        # Premium status
        if user.is_premium:
            text += "**Premium:** ✅ Yes\n"
        else:
            text += "**Premium:** ❌ No\n"
        
        # Bot status
        if user.is_bot:
            text += "**Bot:** ✅ Yes\n"
        
        # Verified status
        if user.is_verified:
            text += "**Verified:** ✅ Yes\n"
        
        # Scam/Fake status
        if user.is_scam:
            text += "**Scam:** ⚠️ Yes\n"
        if user.is_fake:
            text += "**Fake:** ⚠️ Yes\n"
        
        # Get common chats count (only works in private)
        if message.chat.type == ChatType.PRIVATE:
            try:
                common = await client.get_common_chats(user_id)
                text += f"**Common Groups:** {len(common)}\n"
            except Exception:
                pass
        
        # Check if user is in current chat (for groups)
        if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                member = await client.get_chat_member(message.chat.id, user_id)
                text += f"**Status:** {member.status.name.replace('_', ' ').title()}\n"
            except Exception:
                pass
        
        await message.reply(text)
        
    except Exception as e:
        await message.reply(f"❌ Failed to get user info: {str(e)}")
