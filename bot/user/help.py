"""
Help command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from bot.utils.buttons import help_buttons, back_button


HELP_MAIN = """
📚 **Help Menu**

Select a category below to see available commands.

**Categories:**
👮 Admin - Group management commands
👤 User - General user commands  
🎵 Music - Music player controls
🎮 Games - Fun games to play
"""

HELP_ADMIN = """
👮 **Admin Commands**

**Moderation:**
• `/ban` - Ban a user
• `/unban` - Unban a user
• `/kick` - Kick a user
• `/mute [time]` - Mute a user
• `/unmute` - Unmute a user

**Warnings:**
• `/warn` - Warn a user
• `/unwarn` - Remove a warn
• `/warns` - View user warns
• `/resetwarns` - Clear all warns

**Messages:**
• `/pin [silent]` - Pin a message
• `/unpin [all]` - Unpin message(s)
• `/purge` - Delete messages
• `/del` - Delete single message

**Settings:**
• `/slowmode <sec>` - Set slowmode
• `/lock <type>` - Lock content type
• `/unlock <type>` - Unlock content
• `/locks` - View active locks

_Reply to a user or provide ID/username_
"""

HELP_USER = """
👤 **User Commands**

• `/start` - Start the bot
• `/help` - Show this help menu
• `/id` - Get user/chat ID
• `/ping` - Check bot latency
• `/info` - Get user information
• `/avatar` - Get user's profile photo
• `/meme` - Get a random meme
• `/ask <question>` - Ask AI a question
"""

HELP_MUSIC = """
🎵 **Music Commands**

• `/play <song>` - Play a song
• `/pause` - Pause playback
• `/resume` - Resume playback
• `/skip` - Skip current song
• `/stop` - Stop and leave
• `/queue` - View song queue

_Note: Bot must be in voice chat_
"""

HELP_GAMES = """
🎮 **Game Commands**

**Hangman:**
• `/hangman` - Start hangman game
• Guess letters in chat

**Trivia:**
• `/trivia` - Start trivia quiz
• Answer with A, B, C, or D

**Word Game:**
• `/wordgame` - Start word chain
• Reply with words starting with last letter
"""


@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    await message.reply(HELP_MAIN, reply_markup=help_buttons())


@Client.on_callback_query(filters.regex("^help_main$"))
async def help_main_callback(client: Client, callback: CallbackQuery):
    """Handle help main callback"""
    await callback.message.edit_text(HELP_MAIN, reply_markup=help_buttons())
    await callback.answer()


@Client.on_callback_query(filters.regex("^help_admin$"))
async def help_admin_callback(client: Client, callback: CallbackQuery):
    """Handle admin help callback"""
    await callback.message.edit_text(HELP_ADMIN, reply_markup=back_button("help_main"))
    await callback.answer()


@Client.on_callback_query(filters.regex("^help_user$"))
async def help_user_callback(client: Client, callback: CallbackQuery):
    """Handle user help callback"""
    await callback.message.edit_text(HELP_USER, reply_markup=back_button("help_main"))
    await callback.answer()


@Client.on_callback_query(filters.regex("^help_music$"))
async def help_music_callback(client: Client, callback: CallbackQuery):
    """Handle music help callback"""
    await callback.message.edit_text(HELP_MUSIC, reply_markup=back_button("help_main"))
    await callback.answer()


@Client.on_callback_query(filters.regex("^help_games$"))
async def help_games_callback(client: Client, callback: CallbackQuery):
    """Handle games help callback"""
    await callback.message.edit_text(HELP_GAMES, reply_markup=back_button("help_main"))
    await callback.answer()
