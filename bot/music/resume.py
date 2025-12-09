"""
Resume music command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("resume") & filters.group)
async def resume_music(client: Client, message: Message):
    """Resume paused playback"""
    try:
        # Full implementation would use py-tgcalls:
        # await pytgcalls.resume_stream(message.chat.id)
        
        await message.reply(
            "▶️ **Playback Resumed**\n\n"
            "_Note: Full streaming requires py-tgcalls setup._"
        )
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_callback_query(filters.regex("^music_resume$"))
async def resume_callback(client, callback):
    """Handle resume button callback"""
    try:
        await callback.answer("▶️ Resumed!")
        await callback.message.edit_text(
            callback.message.text.replace("\n\n⏸ **Paused**", "") + "\n\n▶️ **Playing**"
        )
    except Exception:
        await callback.answer("Failed to resume", show_alert=True)
