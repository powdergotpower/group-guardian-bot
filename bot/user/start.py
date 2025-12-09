"""
Start command handler
"""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatType
from bot.utils.buttons import start_buttons, help_buttons, back_button


START_TEXT = """
👋 **Hello {name}!**

I'm a powerful **Group Management Bot** that helps you manage your Telegram groups efficiently.

🔹 **Admin Commands** - Ban, kick, mute, warn users
🔹 **User Commands** - Get info, check ping, and more
🔹 **Music Player** - Play music in voice chats
🔹 **Fun Games** - Hangman, trivia, word games

Click the buttons below to learn more!
"""

ABOUT_TEXT = """
ℹ️ **About This Bot**

**Version:** 1.0.0
**Framework:** Pyrogram v2
**Language:** Python 3.10+

**Features:**
• Full admin controls
• Warning system with auto-ban
• Content lock system
• Music streaming
• Interactive games

**Support:**
Join our support group for help!

Made with ❤️
"""


@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user_name = message.from_user.first_name if message.from_user else "User"
    
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(
            START_TEXT.format(name=user_name),
            reply_markup=start_buttons()
        )
    else:
        await message.reply(
            f"👋 Hi {user_name}! I'm online and ready to help manage this group.\n"
            "Use /help to see available commands."
        )


@Client.on_callback_query(filters.regex("^start$"))
async def start_callback(client: Client, callback: CallbackQuery):
    """Handle start button callback"""
    user_name = callback.from_user.first_name if callback.from_user else "User"
    
    await callback.message.edit_text(
        START_TEXT.format(name=user_name),
        reply_markup=start_buttons()
    )
    await callback.answer()


@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(client: Client, callback: CallbackQuery):
    """Handle about button callback"""
    await callback.message.edit_text(
        ABOUT_TEXT,
        reply_markup=back_button("start")
    )
    await callback.answer()
