\"""
Antiflood handler - prevent message flooding
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from collections import defaultdict
from database import ChatSettings, get_session
from sqlalchemy import select
import time

# Store flood data: {chat_id: {user_id: [timestamps]}}
flood_data = defaultdict(lambda: defaultdict(list))

# Flood check interval
FLOOD_TIME = 5  # seconds

async def check_flood(chat_id: int, user_id: int, limit: int) -> bool:
    """Check if user is flooding"""
    now = time.time()
    user_messages = flood_data[chat_id][user_id]
    
    # Remove old timestamps
    user_messages[:] = [t for t in user_messages if now - t < FLOOD_TIME]
    
    # Add current message
    user_messages.append(now)
    
    return len(user_messages) > limit


@Client.on_message(filters.group & filters.text)
async def flood_handler(client: Client, message: Message):
    """Check for flood and restrict user if needed"""
    if not message.from_user:
        return
    
    # Skip if user is admin
    from handlers.moderation import is_admin
    if await is_admin(message.chat.id, message.from_user.id, client):
        return
    
    # Get chat settings
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == message.chat.id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings or not settings.antiflood_enabled:
            return
        
        limit = settings.antiflood_limit
        break
    
    # Check flood
    if await check_flood(message.chat.id, message.from_user.id, limit):
        try:
            # Mute the user
            from pyrogram.types import ChatPermissions
            await client.restrict_chat_member(
                message.chat.id,
                message.from_user.id,
                ChatPermissions(can_send_messages=False)
            )
            await message.reply(
                f"🚫 {message.from_user.first_name} muted for flooding!"
            )
        except:
            pass

# Enable/Disable antiflood command
@Client.on_message(filters.command("antiflood") & filters.group)
async def antiflood_handler(client: Client, message: Message):
    """Toggle antiflood on/off"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    # Parse command
    if len(message.command) > 1:
        try:
            limit = int(message.command[1])
        except:
            limit = 5
    else:
        limit = 5
    
    # Update settings
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            settings = ChatSettings(
                chat_id=chat_id,
                antiflood_enabled=True,
                antiflood_limit=limit
            )
            session.add(settings)
        else:
            settings.antiflood_enabled = not settings.antiflood_enabled
            settings.antiflood_limit = limit
        
        await session.commit()
        
        status = "enabled" if settings.antiflood_enabled else "disabled"
        await message.reply(
            f"✅ AntiFlood {status}!\nLimit: {limit} messages per {FLOOD_TIME} seconds"
        )
        break