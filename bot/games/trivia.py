"""
Trivia game handler
"""
import random
import html
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.database import db
from bot.utils.helpers import fetch_json


async def get_trivia_question() -> dict:
    """Fetch a trivia question from Open Trivia DB"""
    data = await fetch_json("https://opentdb.com/api.php?amount=1&type=multiple")
    
    if not data or data.get("response_code") != 0:
        return None
    
    result = data["results"][0]
    
    # Decode HTML entities
    question = html.unescape(result["question"])
    correct = html.unescape(result["correct_answer"])
    incorrect = [html.unescape(a) for a in result["incorrect_answers"]]
    
    # Shuffle answers
    answers = incorrect + [correct]
    random.shuffle(answers)
    correct_index = answers.index(correct)
    
    return {
        "question": question,
        "answers": answers,
        "correct_index": correct_index,
        "category": result["category"],
        "difficulty": result["difficulty"]
    }


@Client.on_message(filters.command("trivia") & filters.group)
async def start_trivia(client: Client, message: Message):
    """Start a trivia question"""
    chat_id = message.chat.id
    
    # Handle stop command
    if len(message.command) > 1 and message.command[1].lower() == "stop":
        await db.clear_game_state(chat_id, "trivia")
        await message.reply("🛑 Trivia ended!")
        return
    
    status = await message.reply("🔄 Fetching trivia question...")
    
    try:
        trivia = await get_trivia_question()
        
        if not trivia:
            await status.edit_text("❌ Failed to fetch trivia. Try again!")
            return
        
        # Create answer buttons
        buttons = []
        labels = ["A", "B", "C", "D"]
        for i, answer in enumerate(trivia["answers"]):
            buttons.append([InlineKeyboardButton(
                f"{labels[i]}. {answer}",
                callback_data=f"trivia_{i}"
            )])
        
        # Save game state
        state = {
            "correct_index": trivia["correct_index"],
            "answers": trivia["answers"],
            "answered_by": []
        }
        await db.set_game_state(chat_id, "trivia", state)
        
        difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
        
        await status.edit_text(
            f"❓ **Trivia Time!**\n\n"
            f"**Category:** {trivia['category']}\n"
            f"**Difficulty:** {difficulty_emoji.get(trivia['difficulty'], '⚪')} {trivia['difficulty'].title()}\n\n"
            f"**Question:**\n{trivia['question']}\n\n"
            f"_Click a button to answer!_",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")


@Client.on_callback_query(filters.regex(r"^trivia_(\d)$"))
async def handle_trivia_answer(client, callback):
    """Handle trivia answer"""
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id
    answer_index = int(callback.data.split("_")[1])
    
    state = await db.get_game_state(chat_id, "trivia")
    if not state:
        await callback.answer("This trivia has expired!", show_alert=True)
        return
    
    # Check if already answered
    if user_id in state["answered_by"]:
        await callback.answer("You already answered!", show_alert=True)
        return
    
    # Record answer
    state["answered_by"].append(user_id)
    await db.set_game_state(chat_id, "trivia", state)
    
    correct_index = state["correct_index"]
    correct_answer = state["answers"][correct_index]
    
    if answer_index == correct_index:
        await callback.answer("✅ Correct!", show_alert=True)
        await callback.message.reply(
            f"🎉 **{callback.from_user.first_name}** got it right!\n\n"
            f"**Answer:** {correct_answer}\n\n"
            f"Use `/trivia` for another question!"
        )
    else:
        selected_answer = state["answers"][answer_index]
        await callback.answer(f"❌ Wrong! The answer was: {correct_answer}", show_alert=True)
    
    # Clear game after first answer
    await db.clear_game_state(chat_id, "trivia")
