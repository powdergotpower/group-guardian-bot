"""
Inline keyboard button utilities
"""
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_buttons() -> InlineKeyboardMarkup:
    """Generate start menu buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Help", callback_data="help_main"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("➕ Add to Group", url="https://t.me/YOUR_BOT?startgroup=true")
        ]
    ])


def help_buttons() -> InlineKeyboardMarkup:
    """Generate help menu buttons"""
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


def back_button(callback_data: str = "help_main") -> InlineKeyboardMarkup:
    """Generate back button"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data=callback_data)]
    ])


def confirm_buttons(action: str, target_id: int) -> InlineKeyboardMarkup:
    """Generate confirmation buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Yes", callback_data=f"confirm_{action}_{target_id}"),
            InlineKeyboardButton("❌ No", callback_data="cancel")
        ]
    ])


def game_buttons(game_type: str) -> InlineKeyboardMarkup:
    """Generate game control buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎮 New Game", callback_data=f"game_{game_type}_new"),
            InlineKeyboardButton("🛑 End Game", callback_data=f"game_{game_type}_end")
        ]
    ])


def music_buttons() -> InlineKeyboardMarkup:
    """Generate music control buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏸ Pause", callback_data="music_pause"),
            InlineKeyboardButton("▶️ Resume", callback_data="music_resume"),
            InlineKeyboardButton("⏭ Skip", callback_data="music_skip")
        ],
        [
            InlineKeyboardButton("🛑 Stop", callback_data="music_stop"),
            InlineKeyboardButton("📜 Queue", callback_data="music_queue")
        ]
    ])
