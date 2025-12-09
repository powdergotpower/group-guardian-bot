"""
Hangman game handler
"""
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database import db

# Word list for hangman
WORDS = [
    "python", "telegram", "programming", "developer", "keyboard",
    "computer", "algorithm", "database", "function", "variable",
    "internet", "software", "hardware", "network", "security",
    "encryption", "protocol", "framework", "library", "module"
]

HANGMAN_STAGES = [
    """
    ┌───┐
    │   │
    │   
    │   
    │   
    └───┴──
    """,
    """
    ┌───┐
    │   │
    │   O
    │   
    │   
    └───┴──
    """,
    """
    ┌───┐
    │   │
    │   O
    │   │
    │   
    └───┴──
    """,
    """
    ┌───┐
    │   │
    │   O
    │  /│
    │   
    └───┴──
    """,
    """
    ┌───┐
    │   │
    │   O
    │  /│\\
    │   
    └───┴──
    """,
    """
    ┌───┐
    │   │
    │   O
    │  /│\\
    │  / 
    └───┴──
    """,
    """
    ┌───┐
    │   │
    │   O
    │  /│\\
    │  / \\
    └───┴──
    """
]


def get_display_word(word: str, guessed: set) -> str:
    """Get the word with unguessed letters hidden"""
    return " ".join(c if c in guessed else "_" for c in word)


@Client.on_message(filters.command("hangman") & filters.group)
async def start_hangman(client: Client, message: Message):
    """Start a new hangman game"""
    chat_id = message.chat.id
    
    # Check if game already in progress
    state = await db.get_game_state(chat_id, "hangman")
    if state:
        await message.reply(
            "🎮 A game is already in progress!\n"
            "Use `/hangman stop` to end it."
        )
        return
    
    # Handle stop command
    if len(message.command) > 1 and message.command[1].lower() == "stop":
        await db.clear_game_state(chat_id, "hangman")
        await message.reply("🛑 Hangman game ended!")
        return
    
    # Start new game
    word = random.choice(WORDS).lower()
    state = {
        "word": word,
        "guessed": [],
        "wrong": 0,
        "started_by": message.from_user.id
    }
    await db.set_game_state(chat_id, "hangman", state)
    
    display = get_display_word(word, set())
    
    await message.reply(
        f"🎮 **Hangman Game Started!**\n\n"
        f"```{HANGMAN_STAGES[0]}```\n"
        f"**Word:** `{display}`\n"
        f"**Letters:** {len(word)}\n\n"
        f"Guess a letter by typing it in chat!\n"
        f"Use `/hangman stop` to end the game."
    )


@Client.on_message(filters.text & filters.group & ~filters.command([""]))
async def handle_hangman_guess(client: Client, message: Message):
    """Handle letter guesses"""
    chat_id = message.chat.id
    
    # Check if game in progress
    state = await db.get_game_state(chat_id, "hangman")
    if not state:
        return
    
    # Check if it's a single letter
    text = message.text.lower().strip()
    if len(text) != 1 or not text.isalpha():
        return
    
    letter = text
    word = state["word"]
    guessed = set(state["guessed"])
    wrong = state["wrong"]
    
    # Check if already guessed
    if letter in guessed:
        await message.reply(f"⚠️ You already guessed '{letter}'!")
        return
    
    # Add to guessed letters
    guessed.add(letter)
    state["guessed"] = list(guessed)
    
    # Check if correct
    if letter in word:
        display = get_display_word(word, guessed)
        
        # Check if won
        if "_" not in display:
            await db.clear_game_state(chat_id, "hangman")
            await message.reply(
                f"🎉 **Congratulations!**\n\n"
                f"**{message.from_user.first_name}** guessed the word!\n"
                f"**Word:** `{word}`\n\n"
                f"Use `/hangman` to play again!"
            )
            return
        
        await message.reply(
            f"✅ Correct!\n\n"
            f"```{HANGMAN_STAGES[wrong]}```\n"
            f"**Word:** `{display}`\n"
            f"**Guessed:** {', '.join(sorted(guessed))}"
        )
    else:
        wrong += 1
        state["wrong"] = wrong
        
        # Check if lost
        if wrong >= len(HANGMAN_STAGES) - 1:
            await db.clear_game_state(chat_id, "hangman")
            await message.reply(
                f"💀 **Game Over!**\n\n"
                f"```{HANGMAN_STAGES[-1]}```\n"
                f"**The word was:** `{word}`\n\n"
                f"Use `/hangman` to play again!"
            )
            return
        
        display = get_display_word(word, guessed)
        await message.reply(
            f"❌ Wrong! {len(HANGMAN_STAGES) - 1 - wrong} tries left.\n\n"
            f"```{HANGMAN_STAGES[wrong]}```\n"
            f"**Word:** `{display}`\n"
            f"**Guessed:** {', '.join(sorted(guessed))}"
        )
    
    # Save state
    await db.set_game_state(chat_id, "hangman", state)
