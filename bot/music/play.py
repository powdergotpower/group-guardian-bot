"""
Music play command handler

NOTE: Full voice chat streaming requires py-tgcalls which may have
compatibility issues on some systems. This implementation provides
a basic audio file sending fallback.

For full streaming support, install:
- py-tgcalls
- ffmpeg

And uncomment the streaming code below.
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database import db
from bot.utils.buttons import music_buttons
import aiohttp


@Client.on_message(filters.command("play") & filters.group)
async def play_music(client: Client, message: Message):
    """Play music in voice chat"""
    if len(message.command) < 2:
        await message.reply(
            "❌ Please provide a song name or YouTube URL.\n"
            "Usage: `/play <song name or URL>`"
        )
        return
    
    query = " ".join(message.command[1:])
    
    status = await message.reply("🔍 Searching for your song...")
    
    try:
        # Search for the song
        # Note: For full implementation, you would:
        # 1. Search YouTube using yt-dlp or youtube-search-python
        # 2. Download/stream the audio
        # 3. Use py-tgcalls to stream to voice chat
        
        # Basic implementation - add to queue
        track = {
            "title": query,
            "requested_by": message.from_user.id,
            "url": None  # Would be filled with actual URL
        }
        
        await db.add_to_queue(message.chat.id, track)
        queue = await db.get_queue(message.chat.id)
        
        await status.edit_text(
            f"🎵 **Added to Queue**\n\n"
            f"**Title:** {query}\n"
            f"**Position:** {len(queue)}\n"
            f"**Requested by:** {message.from_user.first_name}\n\n"
            f"⚠️ _Note: Full voice chat streaming requires additional setup._\n"
            f"_See music/play.py for instructions._",
            reply_markup=music_buttons()
        )
        
        # ============================================
        # FULL STREAMING IMPLEMENTATION (Uncomment when py-tgcalls is installed)
        # ============================================
        # from pytgcalls import PyTgCalls
        # from pytgcalls.types import AudioPiped
        # 
        # # Initialize PyTgCalls (should be done in main.py)
        # # pytgcalls = PyTgCalls(client)
        # # await pytgcalls.start()
        #
        # # Search YouTube
        # from youtubesearchpython import VideosSearch
        # search = VideosSearch(query, limit=1)
        # result = search.result()
        # 
        # if not result['result']:
        #     await status.edit_text("❌ No results found!")
        #     return
        # 
        # video = result['result'][0]
        # url = video['link']
        # title = video['title']
        # duration = video['duration']
        # 
        # # Download audio using yt-dlp
        # import yt_dlp
        # ydl_opts = {
        #     'format': 'bestaudio/best',
        #     'outtmpl': f'downloads/{message.chat.id}.%(ext)s',
        #     'postprocessors': [{
        #         'key': 'FFmpegExtractAudio',
        #         'preferredcodec': 'mp3',
        #     }],
        # }
        # 
        # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #     info = ydl.extract_info(url, download=True)
        #     audio_file = f"downloads/{message.chat.id}.mp3"
        # 
        # # Stream to voice chat
        # await pytgcalls.join_group_call(
        #     message.chat.id,
        #     AudioPiped(audio_file)
        # )
        # 
        # await status.edit_text(
        #     f"🎵 **Now Playing**\n\n"
        #     f"**Title:** {title}\n"
        #     f"**Duration:** {duration}\n"
        #     f"**Requested by:** {message.from_user.first_name}",
        #     reply_markup=music_buttons()
        # )
        # ============================================
        
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")
