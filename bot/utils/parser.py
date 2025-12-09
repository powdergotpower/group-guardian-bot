"""
Message and argument parsing utilities
"""
from typing import Optional, Tuple, Union
from pyrogram.types import Message
from pyrogram import Client


async def extract_user(client: Client, message: Message) -> Tuple[Optional[int], Optional[str]]:
    """
    Extract user ID and reason from message
    Returns (user_id, reason) or (None, None) if not found
    """
    user_id = None
    reason = None
    
    # Check if replying to a message
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        # Get reason from command arguments
        if len(message.command) > 1:
            reason = " ".join(message.command[1:])
    # Check if user ID or username provided as argument
    elif len(message.command) > 1:
        arg = message.command[1]
        
        # Check if it's a user ID
        if arg.isdigit():
            user_id = int(arg)
        # Check if it's a username
        elif arg.startswith("@"):
            try:
                user = await client.get_users(arg)
                user_id = user.id
            except Exception:
                pass
        
        # Get reason from remaining arguments
        if len(message.command) > 2:
            reason = " ".join(message.command[2:])
    
    return user_id, reason


async def extract_time(text: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Extract time duration from text
    Returns (seconds, remaining_text)
    Supports: 1m, 1h, 1d, 1w formats
    """
    if not text:
        return None, None
    
    parts = text.split(None, 1)
    time_str = parts[0].lower()
    remaining = parts[1] if len(parts) > 1 else None
    
    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800
    }
    
    if time_str[-1] in multipliers and time_str[:-1].isdigit():
        seconds = int(time_str[:-1]) * multipliers[time_str[-1]]
        return seconds, remaining
    
    return None, text


def format_time(seconds: int) -> str:
    """Format seconds into human readable time"""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        return f"{seconds // 60} minutes"
    elif seconds < 86400:
        return f"{seconds // 3600} hours"
    else:
        return f"{seconds // 86400} days"


def get_mention(user) -> str:
    """Get user mention string"""
    name = user.first_name or "User"
    return f"[{name}](tg://user?id={user.id})"


def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text
