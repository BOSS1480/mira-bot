\"""
Settings and basic handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from database import ConnectedChats, get_session
from sqlalchemy import select

# Start handler
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    """Handle /start command"""
    await message.reply(
        "👋 Welcome to Mira Bot!\n\n"
        "I'm a powerful group management bot.\n\n"
        "Add me to your group and make me admin to get started!\n\n"
        "Use /help to see all commands."
    )

# Help handler
@Client.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    """Show help menu"""
    help_text = """
📚 *Mira Bot Commands*


*Moderation:*
• /ban - Ban a user
• /unban - Unban a user
• /mute - Mute a user
• /unmute - Unmute a user
• /kick - Kick a user
• /warn - Warn a user
• /warnings - Check warnings
• /clearwarnings - Clear warnings
• /purge - Delete messages
• /report - Report a user

*Welcome:*
• /welcome - Toggle welcome
• /setwelcome - Set welcome message
• /setgoodbye - Set goodbye message

*Protection:*
• /antiflood - Enable antiflood
• /blocklist - Manage blocklist

*Filters:*
• /addfilter - Add filter
• /rmfilter - Remove filter
• /listfilters - List filters

*Rules:*
• /rules - Show rules
• /setrules - Set rules

*Notes:*
• /note - Get a note
• /addnote - Add note
• /rmnote - Remove note
• /listnotes - List notes


*Staff:*
• /promote - Promote to admin
• /demote - Demote from admin
• /staff - List staff

*Settings:*
• /connect - Connect to group
• /setlang - Change language
• /settings - Bot settings

*Info:*
• /id - Get ID
• /info - Get user info
"""
    await message.reply(help_text)

# ID handler
@Client.on_message(filters.command("id"))
async def id_handler(client: Client, message: Message):
    """Get chat or user ID"""
    if message.chat.type == "private":
        await message.reply(f"Your ID: `{message.from_user.id}`")
    else:
        await message.reply(f"Chat ID: `{message.chat.id}`")

# Info handler
@Client.on_message(filters.command("info"))
async def info_handler(client: Client, message: Message):
    """Get user info"""
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    
    if not user:
        await message.reply("User not found!")
        return
    
    text = f"""
👤 *User Info:*

• Name: {user.first_name}
• ID: `{user.id}`
• Username: @{user.username or "None"}
"""
    await message.reply(text)


# Settings handler
@Client.on_message(filters.command("settings") & filters.group)
async def settings_handler(client: Client, message: Message):
    """Show settings"""
    await message.reply("⚙️ Use /connect to connect your private chat with this group.")

# Connect handler
@Client.on_message(filters.command("connect") & filters.private)
async def connect_handler(client: Client, message: Message):
    """Connect private chat to group"""
    if len(message.command) > 1:
        try:
            group_id = int(message.command[1])
        except:
            await message.reply("Invalid group ID")
            return
        
        async for session in get_session():
            connected = ConnectedChats(
                chat_id=message.from_user.id,
                connected_group_id=group_id
            )
            session.add(connected)
            await session.commit()
            await message.reply(f"✅ Connected to group `{group_id}`!")
            break
    else:
        await message.reply("Usage: /connect <group_id>")