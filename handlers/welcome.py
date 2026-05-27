\"""
Welcome and Goodbye message handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from database import ChatSettings, get_session
from sqlalchemy import select
import time

# Helper to format welcome/goodbye message
def format_message(text: str, user, chat) -> str:
    """Format message with placeholders"""
    replacements = {
        "{first}": user.first_name or "User",
        "{last}": user.last_name or "",
        "{fullname}": f"{user.first_name or ''} {user.last_name or ''}".strip(),
        "{username}": f"@{user.username}" if user.username else "no username",
        "{chatname}": chat.title or "this chat",
        "{userid}": str(user.id),
        "{id}": str(user.id)
    }
    
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    
    return text

# Welcome handler
@Client.on_message(filters.new_chat_members & filters.group)
async def welcome_handler(client: Client, message: Message):
    """Send welcome message to new members"""
    chat = message.chat
    
    # Get chat settings
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat.id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings or not settings.welcome_enabled:
            return
        
        welcome_text = settings.welcome_text or "Welcome {first}!"
        break
    
    # Format for each new member
    for user in message.new_chat_members:
        formatted = format_message(welcome_text, user, chat)
        await message.reply(formatted)

# Goodbye handler
@Client.on_message(filters.left_chat_member & filters.group)
async def goodbye_handler(client: Client, message: Message):
    """Send goodbye message when member leaves"""
    chat = message.chat
    user = message.left_chat_member
    
    # Get chat settings
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat.id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings or not settings.goodbye_enabled:
            return
        
        goodbye_text = settings.goodbye_text or "Goodbye {first}!"
        break
    
    formatted = format_message(goodbye_text, user, chat)
    await message.reply(formatted)

# Set welcome message command
@Client.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome_handler(client: Client, message: Message):
    """Set welcome message"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    # Get welcome text from command
    if len(message.command) > 1:
        welcome_text = message.text.split(None, 1)[1]
    else:
        await message.reply("Usage: /setwelcome <message>\n\nPlaceholders: {first}, {last}, {fullname}, {username}, {chatname}, {userid}")
        return
    
    # Save to database
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            settings = ChatSettings(chat_id=chat_id, welcome_text=welcome_text)
            session.add(settings)
        else:
            settings.welcome_text = welcome_text
            settings.welcome_enabled = True
        
        await session.commit()
        await message.reply(f"✅ Welcome message set!\n\n{welcome_text}")
        break

# Set goodbye message command
@Client.on_message(filters.command("setgoodbye") & filters.group)
async def set_goodbye_handler(client: Client, message: Message):
    """Set goodbye message"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if len(message.command) > 1:
        goodbye_text = message.text.split(None, 1)[1]
    else:
        await message.reply("Usage: /setgoodbye <message>")
        return
    
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            settings = ChatSettings(chat_id=chat_id, goodbye_text=goodbye_text, goodbye_enabled=True)
            session.add(settings)
        else:
            settings.goodbye_text = goodbye_text
            settings.goodbye_enabled = True
        
        await session.commit()
        await message.reply(f"✅ Goodbye message set!\n\n{goodbye_text}")
        break

# Welcome toggle command
@Client.on_message(filters.command("welcome") & filters.group)
async def welcome_toggle_handler(client: Client, message: Message):
    """Toggle welcome message on/off"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            settings = ChatSettings(chat_id=chat_id, welcome_enabled=True)
            session.add(settings)
        else:
            settings.welcome_enabled = not settings.welcome_enabled
        
        await session.commit()
        status = "enabled" if settings.welcome_enabled else "disabled"
        await message.reply(f"✅ Welcome message {status}!")
        break