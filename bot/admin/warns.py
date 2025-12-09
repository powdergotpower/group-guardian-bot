"""
Warns list command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.parser import extract_user, get_mention
from bot.database import db
from bot.config import WARN_LIMIT


@Client.on_message(filters.command("warns") & filters.group)
async def list_warns(client: Client, message: Message):
    """List all warns for a user"""
    user_id, _ = await extract_user(client, message)
    
    # If no user specified, show own warns
    if not user_id:
        user_id = message.from_user.id
    
    try:
        # Get user info
        user = await client.get_users(user_id)
        mention = get_mention(user)
        
        # Get warns from database
        warns = await db.get_warns(user_id, message.chat.id)
        warn_count = len(warns)
        
        if warn_count == 0:
            await message.reply(f"✅ {mention} has no warnings.")
            return
        
        # Format warns list
        warns_text = f"⚠️ **Warnings for {mention}**\n"
        warns_text += f"📊 Total: {warn_count}/{WARN_LIMIT}\n\n"
        
        for i, warn in enumerate(warns, 1):
            warns_text += f"**{i}.** {warn['reason']}\n"
            warns_text += f"   └ By: `{warn['warned_by']}` | {warn['timestamp']}\n"
        
        await message.reply(warns_text)
        
    except Exception as e:
        await message.reply(f"❌ Failed to get warns: {str(e)}")
