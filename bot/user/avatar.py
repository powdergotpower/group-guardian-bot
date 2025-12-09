"""
Avatar command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.parser import extract_user


@Client.on_message(filters.command("avatar"))
async def get_avatar(client: Client, message: Message):
    """Get user's profile photo"""
    user_id, _ = await extract_user(client, message)
    
    # If no user specified, show own avatar
    if not user_id:
        user_id = message.from_user.id
    
    try:
        user = await client.get_users(user_id)
        photos = []
        
        async for photo in client.get_chat_photos(user_id, limit=1):
            photos.append(photo)
        
        if not photos:
            await message.reply(f"❌ {user.first_name} has no profile photo.")
            return
        
        # Send the profile photo
        await message.reply_photo(
            photos[0].file_id,
            caption=f"👤 **{user.first_name}'s Profile Photo**\n🆔 ID: `{user.id}`"
        )
        
    except Exception as e:
        await message.reply(f"❌ Failed to get avatar: {str(e)}")


@Client.on_message(filters.command("avatars"))
async def get_all_avatars(client: Client, message: Message):
    """Get all profile photos of a user"""
    user_id, _ = await extract_user(client, message)
    
    if not user_id:
        user_id = message.from_user.id
    
    try:
        user = await client.get_users(user_id)
        photos = []
        
        async for photo in client.get_chat_photos(user_id, limit=10):
            photos.append(photo)
        
        if not photos:
            await message.reply(f"❌ {user.first_name} has no profile photos.")
            return
        
        # Send all photos as a media group
        from pyrogram.types import InputMediaPhoto
        
        if len(photos) == 1:
            await message.reply_photo(
                photos[0].file_id,
                caption=f"👤 **{user.first_name}'s Profile Photo**"
            )
        else:
            media = [InputMediaPhoto(p.file_id) for p in photos]
            media[0] = InputMediaPhoto(
                photos[0].file_id,
                caption=f"👤 **{user.first_name}'s Profile Photos** ({len(photos)} photos)"
            )
            await message.reply_media_group(media)
        
    except Exception as e:
        await message.reply(f"❌ Failed to get avatars: {str(e)}")
