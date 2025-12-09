"""
Word chain game handler
Players must say a word that starts with the last letter of the previous word
"""
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database import db

# Starting words
STARTING_WORDS = [
    "apple", "banana", "cat", "dog", "elephant",
    "flower", "guitar", "house", "island", "jungle"
]


@Client.on_message(filters.command("wordgame") & filters.group)
async def start_wordgame(client: Client, message: Message):
    """Start a word chain game"""
    chat_id = message.chat.id
    
    # Handle stop command
    if len(message.command) > 1 and message.command[1].lower() == "stop":
        state = await db.get_game_state(chat_id, "wordgame")
        if state:
            used_words = state.get("used_words", [])
            await db.clear_game_state(chat_id, "wordgame")
            await message.reply(
                f"🛑 **Word Game Ended!**\n\n"
                f"**Total words:** {len(used_words)}\n"
                f"**Words used:** {', '.join(used_words[-10:])}"
            )
        else:
            await message.reply("No game in progress!")
        return
    
    # Check if game already running
    state = await db.get_game_state(chat_id, "wordgame")
    if state:
        current_word = state.get("current_word", "")
        await message.reply(
            f"🎮 A game is already in progress!\n\n"
            f"**Current word:** `{current_word}`\n"
            f"**Next letter:** `{current_word[-1].upper()}`\n\n"
            f"Use `/wordgame stop` to end it."
        )
        return
    
    # Start new game
    starting_word = random.choice(STARTING_WORDS)
    state = {
        "current_word": starting_word,
        "used_words": [starting_word],
        "last_player": None,
        "scores": {}
    }
    await db.set_game_state(chat_id, "wordgame", state)
    
    await message.reply(
        f"🎮 **Word Chain Game Started!**\n\n"
        f"**Rules:**\n"
        f"• Say a word starting with the last letter of the previous word\n"
        f"• No repeating words\n"
        f"• Single English words only\n\n"
        f"**Starting word:** `{starting_word}`\n"
        f"**Your turn!** Say a word starting with: `{starting_word[-1].upper()}`\n\n"
        f"Use `/wordgame stop` to end the game."
    )


@Client.on_message(filters.text & filters.group & ~filters.command([""]))
async def handle_wordgame(client: Client, message: Message):
    """Handle word game guesses"""
    chat_id = message.chat.id
    
    # Check if game in progress
    state = await db.get_game_state(chat_id, "wordgame")
    if not state:
        return
    
    # Get the word
    word = message.text.lower().strip()
    
    # Validate: single word, letters only
    if " " in word or not word.isalpha():
        return
    
    if len(word) < 2:
        return
    
    current_word = state["current_word"]
    required_letter = current_word[-1].lower()
    used_words = state.get("used_words", [])
    scores = state.get("scores", {})
    user_id = str(message.from_user.id)
    
    # Check if starts with correct letter
    if not word.startswith(required_letter):
        return  # Silently ignore wrong letters
    
    # Check if already used
    if word in used_words:
        await message.reply(f"⚠️ '{word}' was already used! Try another word.")
        return
    
    # Check same player
    if state.get("last_player") == message.from_user.id:
        await message.reply("⏳ Wait for someone else to play!")
        return
    
    # Valid word!
    used_words.append(word)
    scores[user_id] = scores.get(user_id, 0) + 1
    
    state["current_word"] = word
    state["used_words"] = used_words
    state["last_player"] = message.from_user.id
    state["scores"] = scores
    
    await db.set_game_state(chat_id, "wordgame", state)
    
    await message.reply(
        f"✅ **{message.from_user.first_name}:** `{word}`\n\n"
        f"**Next letter:** `{word[-1].upper()}`\n"
        f"**Chain length:** {len(used_words)} words\n"
        f"**Your score:** {scores[user_id]} points"
    )


@Client.on_message(filters.command("wordscore") & filters.group)
async def show_wordgame_score(client: Client, message: Message):
    """Show word game scores"""
    chat_id = message.chat.id
    
    state = await db.get_game_state(chat_id, "wordgame")
    if not state:
        await message.reply("No word game in progress!")
        return
    
    scores = state.get("scores", {})
    used_words = state.get("used_words", [])
    
    if not scores:
        await message.reply("No scores yet!")
        return
    
    # Sort by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    text = "🏆 **Word Game Leaderboard**\n\n"
    
    for i, (user_id, score) in enumerate(sorted_scores[:10], 1):
        try:
            user = await client.get_users(int(user_id))
            name = user.first_name
        except Exception:
            name = f"User {user_id}"
        
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        text += f"{medal} {name}: {score} points\n"
    
    text += f"\n📊 **Chain Length:** {len(used_words)} words"
    
    await message.reply(text)
