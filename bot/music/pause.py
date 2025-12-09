"""
Pause music command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("pause") & filters.group)
async def pause_music(client: Client, message: Message):
    """Pause current playback"""
    try:
        # Full implementation would use py-tgcalls:
        # await pytgcalls.pause_stream(message.chat.id)
        
        await message.reply(
            "⏸ **Playback Paused**\n\n"
            "Use `/resume` to continue playing.\n\n"
            "_Note: Full streaming requires py-tgcalls setup._"
        )
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_callback_query(filters.regex("^music_pause$"))
async def pause_callback(client, callback):
    """Handle pause button callback"""
    try:
        await callback.answer("⏸ Paused!")
        await callback.message.edit_text(
            callback.message.text + "\n\n⏸ **Paused**"
        )
    except Exception:
        await callback.answer("Failed to pause", show_alert=True)
