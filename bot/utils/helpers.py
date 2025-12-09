"""
Helper functions
"""
import aiohttp
from typing import Optional, Dict, Any
from pyrogram.types import Message, ChatMember
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus


async def is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    """Check if user is admin in chat"""
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception:
        return False


async def is_bot_admin(client: Client, chat_id: int) -> bool:
    """Check if bot is admin in chat"""
    try:
        bot = await client.get_me()
        return await is_admin(client, chat_id, bot.id)
    except Exception:
        return False


async def can_restrict(client: Client, chat_id: int) -> bool:
    """Check if bot can restrict members"""
    try:
        bot = await client.get_me()
        member = await client.get_chat_member(chat_id, bot.id)
        if member.status == ChatMemberStatus.OWNER:
            return True
        return member.privileges.can_restrict_members if member.privileges else False
    except Exception:
        return False


async def can_delete(client: Client, chat_id: int) -> bool:
    """Check if bot can delete messages"""
    try:
        bot = await client.get_me()
        member = await client.get_chat_member(chat_id, bot.id)
        if member.status == ChatMemberStatus.OWNER:
            return True
        return member.privileges.can_delete_messages if member.privileges else False
    except Exception:
        return False


async def can_pin(client: Client, chat_id: int) -> bool:
    """Check if bot can pin messages"""
    try:
        bot = await client.get_me()
        member = await client.get_chat_member(chat_id, bot.id)
        if member.status == ChatMemberStatus.OWNER:
            return True
        return member.privileges.can_pin_messages if member.privileges else False
    except Exception:
        return False


async def fetch_json(url: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
    """Fetch JSON from URL"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
    except Exception:
        pass
    return None


async def download_file(url: str, path: str) -> bool:
    """Download file from URL"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(path, 'wb') as f:
                        f.write(await response.read())
                    return True
    except Exception:
        pass
    return False


def split_message(text: str, max_length: int = 4096) -> list:
    """Split long message into chunks"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
        
        # Find a good split point
        split_point = text.rfind('\n', 0, max_length)
        if split_point == -1:
            split_point = text.rfind(' ', 0, max_length)
        if split_point == -1:
            split_point = max_length
        
        chunks.append(text[:split_point])
        text = text[split_point:].lstrip()
    
    return chunks
