"""
Queue command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database import db


@Client.on_message(filters.command("queue") & filters.group)
async def show_queue(client: Client, message: Message):
    """Show the music queue"""
    try:
        queue = await db.get_queue(message.chat.id)
        
        if not queue:
            await message.reply("📭 The queue is empty!\nUse `/play <song>` to add songs.")
            return
        
        text = "🎵 **Music Queue**\n\n"
        
        for i, track in enumerate(queue, 1):
            title = track.get("title", "Unknown")
            requester_id = track.get("requested_by", "Unknown")
            
            if i == 1:
                text += f"▶️ **Now Playing:** {title}\n\n"
                text += "**Up Next:**\n"
            else:
                text += f"{i-1}. {title}\n"
        
        text += f"\n📊 **Total:** {len(queue)} songs"
        
        await message.reply(text)
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_callback_query(filters.regex("^music_queue$"))
async def queue_callback(client, callback):
    """Handle queue button callback"""
    try:
        queue = await db.get_queue(callback.message.chat.id)
        
        if not queue:
            await callback.answer("Queue is empty!", show_alert=True)
            return
        
        text = f"📜 Queue: {len(queue)} songs"
        await callback.answer(text, show_alert=True)
        
    except Exception:
        await callback.answer("Failed to get queue", show_alert=True)
