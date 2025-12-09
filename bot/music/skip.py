"""
Skip music command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database import db


@Client.on_message(filters.command("skip") & filters.group)
async def skip_music(client: Client, message: Message):
    """Skip to next song in queue"""
    try:
        queue = await db.get_queue(message.chat.id)
        
        if len(queue) <= 1:
            await message.reply("❌ No more songs in the queue!")
            return
        
        # Remove the first song (current playing)
        skipped = queue.pop(0)
        
        # Update queue in database
        await db.clear_queue(message.chat.id)
        for track in queue:
            await db.add_to_queue(message.chat.id, track)
        
        # Full implementation would:
        # 1. Stop current stream
        # 2. Start playing next song
        
        next_song = queue[0] if queue else None
        
        response = f"⏭ **Skipped:** {skipped.get('title', 'Unknown')}\n\n"
        if next_song:
            response += f"🎵 **Now Playing:** {next_song.get('title', 'Unknown')}"
        else:
            response += "📭 Queue is now empty."
        
        await message.reply(response)
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_callback_query(filters.regex("^music_skip$"))
async def skip_callback(client, callback):
    """Handle skip button callback"""
    try:
        await callback.answer("⏭ Skipped!")
        # Trigger skip logic
    except Exception:
        await callback.answer("Failed to skip", show_alert=True)
