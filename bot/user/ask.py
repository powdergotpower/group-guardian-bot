"""
Ask AI command handler
Uses free AI API endpoints
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.helpers import fetch_json
import aiohttp


@Client.on_message(filters.command("ask"))
async def ask_ai(client: Client, message: Message):
    """Ask AI a question"""
    if len(message.command) < 2:
        await message.reply(
            "❌ Please provide a question.\n"
            "Usage: `/ask <your question>`"
        )
        return
    
    question = " ".join(message.command[1:])
    
    # Send typing indicator
    await client.send_chat_action(message.chat.id, "typing")
    
    status_msg = await message.reply("🤔 Thinking...")
    
    try:
        # Try using a free AI API (you can replace with your preferred API)
        # Option 1: Use a simple chatbot API
        response = await get_ai_response(question)
        
        if response:
            await status_msg.edit_text(f"🤖 **AI Response:**\n\n{response}")
        else:
            await status_msg.edit_text("❌ Failed to get a response. Please try again.")
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")


async def get_ai_response(question: str) -> str:
    """Get AI response from API"""
    try:
        # Using a free API endpoint
        # You can replace this with your preferred AI API
        async with aiohttp.ClientSession() as session:
            # Option: Use Brainshop API (free chatbot)
            # Register at https://brainshop.ai/ for API keys
            url = "http://api.brainshop.ai/get"
            params = {
                "bid": "YOUR_BRAIN_ID",  # Replace with your brain ID
                "key": "YOUR_API_KEY",    # Replace with your API key
                "uid": "1",
                "msg": question
            }
            
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("cnt", "I couldn't understand that.")
        
        # Fallback: Simple response
        return "⚠️ AI service not configured. Please set up an AI API key."
        
    except Exception:
        return None


@Client.on_message(filters.command("joke"))
async def tell_joke(client: Client, message: Message):
    """Tell a random joke"""
    try:
        data = await fetch_json("https://official-joke-api.appspot.com/random_joke")
        
        if data:
            joke = f"😄 **{data['setup']}**\n\n🎭 {data['punchline']}"
            await message.reply(joke)
        else:
            await message.reply("❌ Couldn't fetch a joke right now.")
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")


@Client.on_message(filters.command("quote"))
async def random_quote(client: Client, message: Message):
    """Get a random inspirational quote"""
    try:
        data = await fetch_json("https://api.quotable.io/random")
        
        if data:
            quote = f"💬 *\"{data['content']}\"*\n\n— **{data['author']}**"
            await message.reply(quote)
        else:
            await message.reply("❌ Couldn't fetch a quote right now.")
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
