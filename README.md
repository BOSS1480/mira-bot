# 🤖 Mira Bot

A powerful Telegram group management bot inspired by **MissRose**.

## ✨ Features

### 🔧 Moderation
- **Ban/Unban** - Ban or unban users from the group
- **Kick** - Remove users from the group
- **Mute/Unmute** - Mute or unmute users temporarily
- **Warn/Warnings** - Warn users and track violations
- **Purge** - Delete multiple messages at once
- **Report** - Report users to admins

### 🛡️ Protection
- **AntiFlood** - Prevent message flooding
- **AntiRaid** - Protect against raid attacks
- **Blocklist** - Auto-delete messages with blocked words

### 👋 Welcome/Goodbye
- **Welcome Messages** - Customizable welcome for new members
- **Goodbye Messages** - Customizable goodbye when members leave
- **Placeholders**: `{first}`, `{last}`, `{fullname}`, `{username}`, `{chatname}`, `{userid}`, `{rules}`

### 🔍 Filters
- **Auto-replies** - Respond to specific keywords
- **Blocklist** - Block specific words/phrases

### 📜 Rules
- **Set Rules** - Define group rules
- **View Rules** - Display rules to users
- **Send Rules** - Send rules privately to users

### 📝 Notes
- **Add Notes** - Save useful information
- **List Notes** - View all notes
- **Get Notes** - Retrieve specific notes

### 👥 Staff Management
- **Promote** - Make users admins
- **Demote** - Remove admin rights
- **Staff List** - View all admins

### ⚙️ Settings
- **Connection** - Connect private chat with bot
- **Language** - Change bot language (30+ languages)
- **Settings** - Configure various options

### 📋 Additional
- **ID** - Get chat/user ID
- **Info** - Get user information
- **Pin/Unpin** - Pin messages
- **Polls** - Create polls

## 🚀 Deployment

### Prerequisites
- Python 3.10+
- Telegram Bot Token

### Installation

```bash
# Clone the repository
git clone https://github.com/BOSS1480/mira-bot.git
cd mira-bot

# Install dependencies
pip install -r requirements.txt

# Configure bot
cp .env.example .env
# Edit .env with your bot token

# Run the bot
python bot.py
```

## 📚 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help menu |
| `/id` | Get chat/user ID |
| `/ban` | Ban a user |
| `/unban` | Unban a user |
| `/mute` | Mute a user |
| `/unmute` | Unmute a user |
| `/kick` | Kick a user |
| `/warn` | Warn a user |
| `/warnings` | Check user warnings |
| `/clearwarnings` | Clear user warnings |
| `/purge` | Delete messages |
| `/welcome` | Set welcome message |
| `/goodbye` | Set goodbye message |
| `/antiflood` | Enable/disable antiflood |
| `/filter` | Add/remove filters |
| `/blocklist` | Manage blocklist |
| `/rules` | Show group rules |
| `/setrules` | Set group rules |
| `/note` | Manage notes |
| `/promote` | Promote user to admin |
| `/demote` | Remove admin rights |
| `/staff` | List all admins |
| `/setlang` | Change language |
| `/settings` | Bot settings |

## 🌐 Supported Languages

- English
- Hebrew
- Arabic
- Spanish
- Russian
- And 30+ more...


## 📝 License

MIT License

## 👨‍💻 Developed by

**Mira AI** - Your personal AI assistant