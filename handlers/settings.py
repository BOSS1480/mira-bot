\"""
Settings and basic handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from config import BOT_NAME, BOT_USERNAME


# Start command (private)
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    """Handle /start command"""
    await message.reply(
        f"👋 Welcome to {BOT_NAME}!\n\n"
        f"I'm a powerful group management bot.\n\n"
        f"Add me to your group and make me admin to get started!\n\n"
        f"Use /help to see all commands."
    )

# Help command
@Client.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    """Show help menu"""
    help_text = """
📖 *Help Menu*

*Moderation:*
• /ban - Ban a user
• /unban - Unban a user
• /kick - Kick a user
• /mute - Mute a user
• /unmute - Unmute a user
• /warn - Warn a user
• /warnings - Check warnings
• /clearwarnings - Clear warnings
• /purge - Delete messages

*Settings:*
• /welcome - Toggle welcome
• /setwelcome - Set welcome message
• /setgoodbye - Set goodbye message
• /setrules - Set group rules
• /rules - Show rules
• /antiflood - Toggle antiflood
• /addfilter - Add filter
• /rmfilter - Remove filter
• /listfilters - List filters
• /blocklist - Manage blocklist

*Notes:*
• /note - Get a note
• /addnote - Add a note
• /rmnote - Remove a note
• /notes - List notes

*Staff:*
• /promote - Promote to admin
• /demote - Demote admin
• /staff - List staff

*Other:*
• /id - Get chat/user ID
• /help - Show this menu
• /setlang - Change language
"""
    await message.reply(help_text, parse_mode="markdown")

# ID command
@Client.on_message(filters.command("id"))
async def id_handler(client: Client, message: Message):
    """Get chat or user ID"""
    if message.chat.type == "private":
        await message.reply(f"Your ID: `{message.from_user.id}`")
    else:
        text = f"📛 Chat ID: `{message.chat.id}`\n"
        if message.reply_to_message:
            text += f"👤 User ID: `{message.reply_to_message.from_user.id}`"
        await message.reply(text)

# Settings command
@Client.on_message(filters.command("settings") & filters.group)
async def settings_handler(client: Client, message: Message):
    """Show chat settings"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    from database import ChatSettings, get_session
    from sqlalchemy import select
    
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if settings:
            text = f"⚙️ *Settings for {message.chat.title}:*\n\n"
            text += f"Welcome: {'✅' if settings.welcome_enabled else '❌'}\n"
            text += f"Goodbye: {'✅' if settings.goodbye_enabled else '❌'}\n"
            text += f"Antiflood: {'✅' if settings.antiflood_enabled else '❌'}\n"
            text += f"Language: {settings.language}\n"
            await message.reply(text, parse_mode="markdown")
        else:
            await message.reply("No settings configured yet!")
        break

# Connect command
@Client.on_message(filters.command("connect") & filters.private)
async def connect_handler(client: Client, message: Message):
    """Connect to a group for settings"""
    if len(message.command) > 1:
        try:
            chat_id = int(message.command[1])
            await message.reply(f"Connected to chat {chat_id}!")
        except:
            await message.reply("Invalid chat ID")
    else:
        await message.reply("Usage: /connect <chat_id>")