"""
Telegram Group Management Bot
Main entry point
"""

import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from config import API_ID, API_HASH, BOT_TOKEN, WARN_LIMIT, LOCKABLE_TYPES
from database import Database
import time
import random
import html
import aiohttp

# Initialize database
db = Database()

# Initialize bot client
app = Client(
    name="group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# ============ HELPER FUNCTIONS ============

def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Help", callback_data="help_main"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("➕ Add to Group", url="https://t.me/TheAnamikasbot?startgroup=true")
        ]
    ])


def help_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👮 Admin", callback_data="help_admin"),
            InlineKeyboardButton("👤 User", callback_data="help_user")
        ],
        [
            InlineKeyboardButton("🎵 Music", callback_data="help_music"),
            InlineKeyboardButton("🎮 Games", callback_data="help_games")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="start")
        ]
    ])


def back_button(callback_data="help_main"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data=callback_data)]
    ])


def get_mention(user):
    name = user.first_name or "User"
    return f"[{name}](tg://user?id={user.id})"


async def extract_user(client, message):
    user_id = None
    reason = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if len(message.command) > 1:
            reason = " ".join(message.command[1:])
    elif len(message.command) > 1:
        arg = message.command[1]
        if arg.isdigit():
            user_id = int(arg)
        elif arg.startswith("@"):
            try:
                user = await client.get_users(arg)
                user_id = user.id
            except:
                pass
        if len(message.command) > 2:
            reason = " ".join(message.command[2:])
    
    return user_id, reason


async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False


async def fetch_json(url, params=None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
    except:
        pass
    return None


# ============ START & HELP ============

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

Made with ❤️
"""

HELP_ADMIN = """
👮 **Admin Commands**

• `/ban` - Ban a user
• `/unban` - Unban a user
• `/kick` - Kick a user
• `/mute` - Mute a user
• `/unmute` - Unmute a user
• `/warn` - Warn a user
• `/unwarn` - Remove a warn
• `/warns` - View user warns
• `/pin` - Pin a message
• `/unpin` - Unpin message
• `/purge` - Delete messages
• `/slowmode <sec>` - Set slowmode
• `/lock <type>` - Lock content
• `/unlock <type>` - Unlock content

_Reply to a user or provide ID_
"""

HELP_USER = """
👤 **User Commands**

• `/start` - Start the bot
• `/help` - Show help menu
• `/id` - Get user/chat ID
• `/ping` - Check bot latency
• `/info` - Get user information
• `/avatar` - Get profile photo
• `/meme` - Get a random meme
"""

HELP_MUSIC = """
🎵 **Music Commands**

• `/play <song>` - Play a song
• `/pause` - Pause playback
• `/resume` - Resume playback
• `/skip` - Skip current song
• `/stop` - Stop and clear queue
• `/queue` - View song queue
"""

HELP_GAMES = """
🎮 **Game Commands**

• `/hangman` - Start hangman
• `/trivia` - Trivia quiz
• `/wordgame` - Word chain game
"""


@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_name = message.from_user.first_name if message.from_user else "User"
    
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(START_TEXT.format(name=user_name), reply_markup=start_buttons())
    else:
        await message.reply(f"👋 Hi {user_name}! Use /help to see commands.")


@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await message.reply("📚 **Help Menu**\n\nSelect a category:", reply_markup=help_buttons())


@app.on_callback_query(filters.regex("^start$"))
async def start_callback(client, callback: CallbackQuery):
    user_name = callback.from_user.first_name if callback.from_user else "User"
    await callback.message.edit_text(START_TEXT.format(name=user_name), reply_markup=start_buttons())
    await callback.answer()


@app.on_callback_query(filters.regex("^about$"))
async def about_callback(client, callback: CallbackQuery):
    await callback.message.edit_text(ABOUT_TEXT, reply_markup=back_button("start"))
    await callback.answer()


@app.on_callback_query(filters.regex("^help_main$"))
async def help_main_callback(client, callback: CallbackQuery):
    await callback.message.edit_text("📚 **Help Menu**\n\nSelect a category:", reply_markup=help_buttons())
    await callback.answer()


@app.on_callback_query(filters.regex("^help_admin$"))
async def help_admin_callback(client, callback: CallbackQuery):
    await callback.message.edit_text(HELP_ADMIN, reply_markup=back_button("help_main"))
    await callback.answer()


@app.on_callback_query(filters.regex("^help_user$"))
async def help_user_callback(client, callback: CallbackQuery):
    await callback.message.edit_text(HELP_USER, reply_markup=back_button("help_main"))
    await callback.answer()


@app.on_callback_query(filters.regex("^help_music$"))
async def help_music_callback(client, callback: CallbackQuery):
    await callback.message.edit_text(HELP_MUSIC, reply_markup=back_button("help_main"))
    await callback.answer()


@app.on_callback_query(filters.regex("^help_games$"))
async def help_games_callback(client, callback: CallbackQuery):
    await callback.message.edit_text(HELP_GAMES, reply_markup=back_button("help_main"))
    await callback.answer()


# ============ USER COMMANDS ============

@app.on_message(filters.command("id"))
async def get_id(client, message: Message):
    text = f"💬 **Chat ID:** `{message.chat.id}`\n"
    if message.from_user:
        text += f"👤 **Your ID:** `{message.from_user.id}`\n"
    if message.reply_to_message and message.reply_to_message.from_user:
        text += f"↩️ **Replied User ID:** `{message.reply_to_message.from_user.id}`\n"
    await message.reply(text)


@app.on_message(filters.command("ping"))
async def ping(client, message: Message):
    start_time = time.time()
    msg = await message.reply("🏓 Pinging...")
    latency = (time.time() - start_time) * 1000
    await msg.edit_text(f"🏓 **Pong!**\n⏱ Latency: `{latency:.2f}ms`")


@app.on_message(filters.command("info"))
async def user_info(client, message: Message):
    user_id, _ = await extract_user(client, message)
    if not user_id:
        user_id = message.from_user.id
    
    try:
        user = await client.get_users(user_id)
        text = f"👤 **User Information**\n\n"
        text += f"**Name:** {user.first_name}"
        if user.last_name:
            text += f" {user.last_name}"
        text += f"\n**ID:** `{user.id}`\n"
        if user.username:
            text += f"**Username:** @{user.username}\n"
        if user.dc_id:
            text += f"**DC ID:** {user.dc_id}\n"
        text += f"**Premium:** {'✅' if user.is_premium else '❌'}\n"
        await message.reply(text)
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@app.on_message(filters.command("avatar"))
async def get_avatar(client, message: Message):
    user_id, _ = await extract_user(client, message)
    if not user_id:
        user_id = message.from_user.id
    
    try:
        photos = []
        async for photo in client.get_chat_photos(user_id, limit=1):
            photos.append(photo)
        
        if photos:
            await message.reply_photo(photos[0].file_id, caption="👤 Profile Photo")
        else:
            await message.reply("❌ No profile photo found.")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@app.on_message(filters.command("meme"))
async def get_meme(client, message: Message):
    try:
        data = await fetch_json("https://meme-api.com/gimme")
        if data and "url" in data:
            await message.reply_photo(data["url"], caption=f"😂 {data.get('title', 'Meme')}")
        else:
            await message.reply("❌ Failed to fetch meme.")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


# ============ ADMIN COMMANDS ============

@app.on_message(filters.command("ban") & filters.group)
async def ban_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    user_id, reason = await extract_user(client, message)
    if not user_id:
        return await message.reply("❌ Reply to a user or provide ID.")
    
    try:
        user = await client.get_users(user_id)
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply(f"🔨 **Banned** {get_mention(user)}" + (f"\n📝 Reason: {reason}" if reason else ""))
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("unban") & filters.group)
async def unban_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    user_id, _ = await extract_user(client, message)
    if not user_id:
        return await message.reply("❌ Provide user ID to unban.")
    
    try:
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply(f"✅ User unbanned!")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("kick") & filters.group)
async def kick_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    user_id, reason = await extract_user(client, message)
    if not user_id:
        return await message.reply("❌ Reply to a user or provide ID.")
    
    try:
        user = await client.get_users(user_id)
        await client.ban_chat_member(message.chat.id, user_id)
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply(f"👢 **Kicked** {get_mention(user)}")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("mute") & filters.group)
async def mute_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    user_id, _ = await extract_user(client, message)
    if not user_id:
        return await message.reply("❌ Reply to a user or provide ID.")
    
    try:
        user = await client.get_users(user_id)
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
        await message.reply(f"🔇 **Muted** {get_mention(user)}")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    user_id, _ = await extract_user(client, message)
    if not user_id:
        return await message.reply("❌ Reply to a user or provide ID.")
    
    try:
        user = await client.get_users(user_id)
        await client.restrict_chat_member(
            message.chat.id, user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True
            )
        )
        await message.reply(f"🔊 **Unmuted** {get_mention(user)}")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("warn") & filters.group)
async def warn_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    user_id, reason = await extract_user(client, message)
    if not user_id:
        return await message.reply("❌ Reply to a user or provide ID.")
    
    try:
        user = await client.get_users(user_id)
        warn_count = await db.add_warn(user_id, message.chat.id, reason or "No reason", message.from_user.id)
        
        if warn_count >= WARN_LIMIT:
            await client.ban_chat_member(message.chat.id, user_id)
            await db.clear_warns(user_id, message.chat.id)
            await message.reply(f"🔨 {get_mention(user)} **BANNED** - Reached {WARN_LIMIT} warns!")
        else:
            await message.reply(f"⚠️ **Warned** {get_mention(user)}\nWarns: {warn_count}/{WARN_LIMIT}")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("unwarn") & filters.group)
async def unwarn_user(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    user_id, _ = await extract_user(client, message)
    if not user_id:
        return await message.reply("❌ Reply to a user or provide ID.")
    
    try:
        removed = await db.remove_warn(user_id, message.chat.id)
        if removed:
            warn_count = await db.get_warn_count(user_id, message.chat.id)
            await message.reply(f"✅ Warn removed. Remaining: {warn_count}/{WARN_LIMIT}")
        else:
            await message.reply("ℹ️ User has no warnings.")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("warns") & filters.group)
async def list_warns(client, message: Message):
    user_id, _ = await extract_user(client, message)
    if not user_id:
        user_id = message.from_user.id
    
    try:
        warns = await db.get_warns(user_id, message.chat.id)
        if warns:
            text = f"⚠️ **Warnings:** {len(warns)}/{WARN_LIMIT}\n\n"
            for i, w in enumerate(warns, 1):
                text += f"{i}. {w['reason']}\n"
            await message.reply(text)
        else:
            await message.reply("✅ No warnings found.")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("pin") & filters.group)
async def pin_message(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    if not message.reply_to_message:
        return await message.reply("❌ Reply to a message to pin.")
    
    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.id)
        await message.reply("📌 Message pinned!")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("unpin") & filters.group)
async def unpin_message(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    try:
        if len(message.command) > 1 and message.command[1].lower() == "all":
            await client.unpin_all_chat_messages(message.chat.id)
            await message.reply("📌 All messages unpinned!")
        else:
            await client.unpin_chat_message(message.chat.id)
            await message.reply("📌 Message unpinned!")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("purge") & filters.group)
async def purge_messages(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    if not message.reply_to_message:
        return await message.reply("❌ Reply to a message to start purging.")
    
    try:
        msg_ids = list(range(message.reply_to_message.id, message.id + 1))
        for i in range(0, len(msg_ids), 100):
            await client.delete_messages(message.chat.id, msg_ids[i:i+100])
        confirm = await message.reply(f"🗑️ Purged {len(msg_ids)} messages.")
        await asyncio.sleep(3)
        await confirm.delete()
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("slowmode") & filters.group)
async def set_slowmode(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    if len(message.command) < 2:
        return await message.reply("Usage: `/slowmode <seconds>` or `/slowmode off`")
    
    arg = message.command[1].lower()
    seconds = 0 if arg in ["off", "0"] else int(arg) if arg.isdigit() else 0
    
    try:
        await client.set_chat_slow_mode_delay(message.chat.id, seconds)
        await message.reply(f"✅ Slowmode {'disabled' if seconds == 0 else f'set to {seconds}s'}")
    except Exception as e:
        await message.reply(f"❌ Failed: {str(e)}")


@app.on_message(filters.command("lock") & filters.group)
async def lock_type(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    if len(message.command) < 2:
        return await message.reply(f"Usage: `/lock <type>`\nTypes: {', '.join(LOCKABLE_TYPES)}")
    
    lock = message.command[1].lower()
    if lock not in LOCKABLE_TYPES:
        return await message.reply(f"Invalid type. Available: {', '.join(LOCKABLE_TYPES)}")
    
    await db.add_lock(message.chat.id, lock)
    await message.reply(f"🔒 Locked: **{lock}**")


@app.on_message(filters.command("unlock") & filters.group)
async def unlock_type(client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("⚠️ You need to be an admin.")
    
    if len(message.command) < 2:
        return await message.reply(f"Usage: `/unlock <type>`")
    
    lock = message.command[1].lower()
    await db.remove_lock(message.chat.id, lock)
    await message.reply(f"🔓 Unlocked: **{lock}**")


@app.on_message(filters.command("locks") & filters.group)
async def list_locks(client, message: Message):
    locks = await db.get_locks(message.chat.id)
    if locks:
        await message.reply(f"🔒 **Active Locks:**\n" + "\n".join([f"• {l}" for l in locks]))
    else:
        await message.reply("✅ No locks active.")


# ============ GAMES ============

HANGMAN_WORDS = ["python", "telegram", "programming", "developer", "computer", "algorithm", "database"]
HANGMAN_STAGES = ["┌───┐\n│   │\n│   \n│   \n│   \n└───┴──", "┌───┐\n│   │\n│   O\n│   \n│   \n└───┴──",
    "┌───┐\n│   │\n│   O\n│   │\n│   \n└───┴──", "┌───┐\n│   │\n│   O\n│  /│\n│   \n└───┴──",
    "┌───┐\n│   │\n│   O\n│  /│\\\n│   \n└───┴──", "┌───┐\n│   │\n│   O\n│  /│\\\n│  / \n└───┴──",
    "┌───┐\n│   │\n│   O\n│  /│\\\n│  / \\\n└───┴──"]


@app.on_message(filters.command("hangman") & filters.group)
async def start_hangman(client, message: Message):
    chat_id = message.chat.id
    
    if len(message.command) > 1 and message.command[1].lower() == "stop":
        await db.clear_game_state(chat_id, "hangman")
        return await message.reply("🛑 Hangman ended!")
    
    state = await db.get_game_state(chat_id, "hangman")
    if state:
        return await message.reply("🎮 Game in progress! Use `/hangman stop` to end.")
    
    word = random.choice(HANGMAN_WORDS)
    state = {"word": word, "guessed": [], "wrong": 0}
    await db.set_game_state(chat_id, "hangman", state)
    
    display = " ".join("_" for _ in word)
    await message.reply(f"🎮 **Hangman Started!**\n\n```{HANGMAN_STAGES[0]}```\n\n**Word:** `{display}`\n\nGuess letters!")


@app.on_message(filters.command("trivia") & filters.group)
async def start_trivia(client, message: Message):
    status = await message.reply("🔄 Loading trivia...")
    
    try:
        data = await fetch_json("https://opentdb.com/api.php?amount=1&type=multiple")
        if not data or data.get("response_code") != 0:
            return await status.edit_text("❌ Failed to fetch trivia.")
        
        result = data["results"][0]
        question = html.unescape(result["question"])
        correct = html.unescape(result["correct_answer"])
        incorrect = [html.unescape(a) for a in result["incorrect_answers"]]
        
        answers = incorrect + [correct]
        random.shuffle(answers)
        correct_idx = answers.index(correct)
        
        await db.set_game_state(message.chat.id, "trivia", {"correct": correct_idx, "answers": answers})
        
        buttons = [[InlineKeyboardButton(f"{['A','B','C','D'][i]}. {a}", callback_data=f"trivia_{i}")] for i, a in enumerate(answers)]
        
        await status.edit_text(
            f"❓ **Trivia**\n\n**Category:** {result['category']}\n\n{question}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")


@app.on_callback_query(filters.regex(r"^trivia_(\d)$"))
async def trivia_answer(client, callback: CallbackQuery):
    state = await db.get_game_state(callback.message.chat.id, "trivia")
    if not state:
        return await callback.answer("Trivia expired!", show_alert=True)
    
    idx = int(callback.data.split("_")[1])
    correct = state["answers"][state["correct"]]
    
    if idx == state["correct"]:
        await callback.answer("✅ Correct!")
        await callback.message.reply(f"🎉 **{callback.from_user.first_name}** got it right!\n\n**Answer:** {correct}")
    else:
        await callback.answer(f"❌ Wrong! Answer: {correct}", show_alert=True)
    
    await db.clear_game_state(callback.message.chat.id, "trivia")


@app.on_message(filters.command("wordgame") & filters.group)
async def start_wordgame(client, message: Message):
    chat_id = message.chat.id
    
    if len(message.command) > 1 and message.command[1].lower() == "stop":
        await db.clear_game_state(chat_id, "wordgame")
        return await message.reply("🛑 Word game ended!")
    
    state = await db.get_game_state(chat_id, "wordgame")
    if state:
        return await message.reply(f"🎮 Game in progress!\nCurrent: `{state['word']}`\nNext letter: `{state['word'][-1].upper()}`")
    
    word = random.choice(["apple", "banana", "cat", "dog", "elephant"])
    await db.set_game_state(chat_id, "wordgame", {"word": word, "used": [word], "last_player": None})
    
    await message.reply(f"🎮 **Word Chain Started!**\n\n**Word:** `{word}`\n**Next letter:** `{word[-1].upper()}`\n\nSay a word starting with that letter!")


# ============ MAIN ============

async def main():
    """Start the bot"""
    await db.init()
    await app.start()
    me = await app.get_me()
    
    print("=" * 40)
    print("Bot started successfully!")
    print(f"Bot username: @{me.username}")
    print("All handlers loaded!")
    print("=" * 40)
    
    await idle()
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
