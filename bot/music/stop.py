"""
Stop music command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database import db


@Client.on_message(filters.command("stop") & filters.group)
async def stop_music(client: Client, message: Message):
    """Stop playback and clear queue"""
    try:
        # Clear the queue
        await db.clear_queue(message.chat.id)
        
        # Full implementation would:
        # await pytgcalls.leave_group_call(message.chat.id)
        
        await message.reply(
            "🛑 **Playback Stopped**\n\n"
            "Queue has been cleared.\n"
            "Use `/play` to start playing again."
        )
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_callback_query(filters.regex("^music_stop$"))
async def stop_callback(client, callback):
    """Handle stop button callback"""
    try:
        await db.clear_queue(callback.message.chat.id)
        await callback.answer("🛑 Stopped!")
        await callback.message.edit_text("🛑 **Playback Stopped**\n\nQueue cleared.")
    except Exception:
        await callback.answer("Failed to stop", show_alert=True)
