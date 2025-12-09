# Telegram Group Management Bot

A powerful Telegram group management bot built with Pyrogram v2.

## Features

- **Admin Commands**: Ban, kick, mute, warn, pin, purge, slowmode, lock/unlock
- **User Commands**: ID, ping, info, avatar, meme, ask AI, jokes, quotes
- **Music Player**: Play, pause, resume, skip, stop, queue (requires additional setup)
- **Games**: Hangman, trivia, word chain game

## Installation

### Prerequisites

- Python 3.10+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- API ID and Hash (from [my.telegram.org](https://my.telegram.org/apps))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/telegram-bot.git
cd telegram-bot
```

2. Install dependencies:
```bash
pip install -r bot/requirements.txt
```

3. Configure environment variables:
```bash
cp bot/.env.example bot/.env
# Edit .env with your credentials
```

4. Run the bot:
```bash
python -m bot.main
```

## Commands

### Admin Commands
| Command | Description |
|---------|-------------|
| `/ban` | Ban a user |
| `/unban` | Unban a user |
| `/kick` | Kick a user |
| `/mute [time]` | Mute a user |
| `/unmute` | Unmute a user |
| `/warn` | Warn a user |
| `/unwarn` | Remove a warn |
| `/warns` | View warnings |
| `/resetwarns` | Clear all warns |
| `/pin` | Pin a message |
| `/unpin` | Unpin message(s) |
| `/purge` | Delete messages |
| `/slowmode` | Set slowmode |
| `/lock` | Lock content type |
| `/unlock` | Unlock content |

### User Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help |
| `/id` | Get IDs |
| `/ping` | Check latency |
| `/info` | User information |
| `/avatar` | Profile photo |
| `/meme` | Random meme |
| `/ask` | Ask AI |

### Games
| Command | Description |
|---------|-------------|
| `/hangman` | Start hangman |
| `/trivia` | Trivia quiz |
| `/wordgame` | Word chain |

## Music Player (Optional)

For full voice chat streaming, you need to install additional dependencies:

```bash
pip install py-tgcalls yt-dlp
```

You'll also need FFmpeg installed on your system.

## Termux Installation

```bash
pkg update && pkg upgrade
pkg install python git
pip install pyrogram aiohttp python-dotenv aiosqlite
git clone https://github.com/yourusername/telegram-bot.git
cd telegram-bot
cp bot/.env.example bot/.env
nano bot/.env  # Add your credentials
python -m bot.main
```

## License

MIT License
