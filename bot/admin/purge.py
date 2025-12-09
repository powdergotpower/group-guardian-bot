"""
Purge command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.filters.admin_filter import admin_filter, can_delete_filter


@Client.on_message(filters.command("purge") & filters.group & admin_filter & can_delete_filter)
async def purge_messages(client: Client, message: Message):
    """Delete messages from reply to current message"""
    if not message.reply_to_message:
        await message.reply("❌ Please reply to a message to start purging from.")
        return
    
    try:
        # Get message range
        start_id = message.reply_to_message.id
        end_id = message.id
        
        # Collect message IDs to delete
        message_ids = list(range(start_id, end_id + 1))
        
        # Delete in batches of 100 (Telegram limit)
        deleted_count = 0
        for i in range(0, len(message_ids), 100):
            batch = message_ids[i:i + 100]
            try:
                await client.delete_messages(message.chat.id, batch)
                deleted_count += len(batch)
            except Exception:
                pass
        
        # Send confirmation (auto-delete after 5 seconds)
        confirm = await message.reply(f"🗑️ Purged {deleted_count} messages.")
        
        # Delete confirmation after delay
        import asyncio
        await asyncio.sleep(5)
        try:
            await confirm.delete()
        except Exception:
            pass
        
    except Exception as e:
        await message.reply(f"❌ Failed to purge: {str(e)}")


@Client.on_message(filters.command("del") & filters.group & admin_filter & can_delete_filter)
async def delete_message(client: Client, message: Message):
    """Delete a single replied message"""
    if not message.reply_to_message:
        await message.reply("❌ Please reply to a message to delete it.")
        return
    
    try:
        await message.reply_to_message.delete()
        await message.delete()
    except Exception as e:
        await message.reply(f"❌ Failed to delete: {str(e)}")
