# Mira Bot - MissRose Clone

A powerful Telegram group management bot inspired by MissRose.

## Features

### Moderation
- **Ban/Unban** - Ban or unban users from the group
- **Kick** - Remove a user from the group
- **Mute/Unmute** - Mute or unmute users temporarily
- **Warn/Warnings** - Warn users and track violations
- **Purge** - Delete multiple messages at once

### Protection
- **Antiflood** - Prevent message flooding
- **AntiRaid** - Protect against mass join attacks
- **CAPTCHA** - Verify new members

### Group Management
- **Welcome/Goodbye** - Custom welcome and goodbye messages
- **Rules** - Set and display group rules
- **Filters** - Auto-respond to keywords
- **Blocklist** - Block certain words
- **Notes** - Save notes for users

### Additional
- **Staff** - Manage group staff
- **Promote/Demote** - Add or remove admins
- **Settings** - Configure bot behavior
- **Multiple Languages** - Support for 30+ languages

## Commands

### Basic
- `/start` - Start the bot
- `/help` - Show help menu
- `/id` - Get chat/user ID

### Moderation
- `/ban` - Ban a user
- `/unban` - Unban a user
- `/kick` - Kick a user
- `/mute` - Mute a user
- `/unmute` - Unmute a user
- `/warn` - Warn a user
- `/warnings` - Check user warnings
- `/clearwarnings` - Clear warnings
- `/purge` - Delete messages

### Settings
- `/antiflood` - Toggle antiflood
- `/welcome` - Set welcome message
- `/goodbye` - Set goodbye message
- `/setrules` - Set group rules
- `/addfilter` - Add a filter
- `/rmfilter` - Remove a filter
- `/setlang` - Change language

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure bot
Edit config.py and add your BOT_TOKEN

# Run the bot
python bot.py
```

## Requirements
- Python 3.8+
- pyrogram
- tgcrypto
- aiosqlite

## License
MIT License