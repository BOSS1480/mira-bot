# 🤖 Mira Bot

Telegram Group Management Bot - MissRose Inspired

## Features

### 👮 Moderation
- **Ban/Unban** - Ban or unban users
- **Kick** - Kick users from group
- **Mute/Unmute** - Mute or unmute users
- **Warn** - Warn users
- **Promote/Demote** - Manage admins

### 🔒 Locks
- Lock stickers, photos, videos, documents, games, inline, polls, voice, videochat, location, contacts, RTL, buttons, eggs

### 📝 Notes & Filters
- Save notes for quick access
- Set keyword filters with auto-replies

### ⚙️ Settings
- Anti-flood protection
- CAPTCHA verification
- Welcome messages
- Group rules
- Multi-language support

### 🚫 Blocklist
- Block specific words in group

## Commands

### Basic
- `/start` - Start the bot
- `/help` - Show help
- `/id` - Get IDs
- `/info` - Get user info
- `/ping` - Check bot status

### Admin
- `/promote` - Promote user
- `/demote` - Demote user
- `/ban` - Ban user
- `/unban` - Unban user
- `/kick` - Kick user
- `/mute` - Mute user
- `/unmute` - Unmute user
- `/warn` - Warn user
- `/warns` - Get user warns
- `/clearwarns` - Clear warns
- `/pin` - Pin message
- `/unpin` - Unpin message
- `/purge` - Delete messages

### Locks
- `/lock <type>` - Lock feature
- `/unlock <type>` - Unlock feature
- `/locks` - Show all locks
- `/grouplock` - Lock all
- `/groupunlock` - Unlock all

### Notes & Filters
- `/note` - Manage notes
- `/filter` - Manage filters
- `/filters` - List filters

### Settings
- `/rules` - Show rules
- `/setrules` - Set rules
- `/welcome` - Set welcome
- `/antiflood` - Anti-flood settings
- `/captcha` - CAPTCHA settings
- `/setlang` - Change language
- `/settings` - Show settings

### Blocklist
- `/blocklist` - Show blocklist
- `/addblock` - Add to blocklist
- `/unblock` - Remove from blocklist


### Staff
- `/staff` - Show staff
- `/adminlist` - Admin list

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BOSS1480/mira-bot.git
cd mira-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your bot token
```

4. Run the bot:
```bash
python bot.py
```

## Docker

```bash
docker build -t mira-bot .
docker run -d mira-bot
```

## Environment Variables

- `BOT_TOKEN` - Your Telegram bot token
- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API hash
- `LOG_CHANNEL` - Log channel ID
- `SUPPORT_GROUP` - Support group username
- `SUPPORT_CHANNEL` - Support channel username

## Languages Supported

- 🇮🇱 Hebrew (he)
- 🇬🇧 English (en)
- 🇸🇦 Arabic (ar)
- 🇪🇸 Spanish (es)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇷🇺 Russian (ru)

## License


MIT License

## Credits

Inspired by [MissRose Bot](https://missrose.org)