"""
Custom admin filter for Pyrogram v2
"""
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ChatType


async def admin_check(_, client, message: Message) -> bool:
    """
    Check if user is admin and bot has required permissions
    """
    # Allow in private chats
    if message.chat.type == ChatType.PRIVATE:
        return True
    
    # Check if user exists
    if not message.from_user:
        return False
    
    try:
        # Get user's member status
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        
        # Check if user is admin or owner
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await message.reply("⚠️ You need to be an admin to use this command.")
            return False
        
        # Get bot's member status
        bot = await client.get_me()
        bot_member = await client.get_chat_member(message.chat.id, bot.id)
        
        # Check if bot is admin
        if bot_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await message.reply("⚠️ I need to be an admin to perform this action.")
            return False
        
        return True
        
    except Exception as e:
        await message.reply(f"❌ Error checking permissions: {str(e)}")
        return False


# Create the filter
admin_filter = filters.create(admin_check)


async def can_restrict_check(_, client, message: Message) -> bool:
    """Check if bot can restrict members"""
    if message.chat.type == ChatType.PRIVATE:
        return False
    
    try:
        bot = await client.get_me()
        member = await client.get_chat_member(message.chat.id, bot.id)
        
        if member.status == ChatMemberStatus.OWNER:
            return True
        
        if member.privileges and member.privileges.can_restrict_members:
            return True
        
        await message.reply("⚠️ I don't have permission to restrict members.")
        return False
        
    except Exception:
        return False


can_restrict_filter = filters.create(can_restrict_check)


async def can_delete_check(_, client, message: Message) -> bool:
    """Check if bot can delete messages"""
    if message.chat.type == ChatType.PRIVATE:
        return False
    
    try:
        bot = await client.get_me()
        member = await client.get_chat_member(message.chat.id, bot.id)
        
        if member.status == ChatMemberStatus.OWNER:
            return True
        
        if member.privileges and member.privileges.can_delete_messages:
            return True
        
        await message.reply("⚠️ I don't have permission to delete messages.")
        return False
        
    except Exception:
        return False


can_delete_filter = filters.create(can_delete_check)
