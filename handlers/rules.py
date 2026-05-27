\"""
Rules handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from database import ChatSettings, get_session
from sqlalchemy import select

# Rules command
@Client.on_message(filters.command("rules") & filters.group)
async def rules_handler(client: Client, message: Message):
    """Show group rules"""
    chat_id = message.chat.id
    
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if settings and settings.rules_text:
            await message.reply(f"📜 *Rules:*\n\n{settings.rules_text}")
        else:
            await message.reply("📜 No rules set yet!\n\nAdmins can set rules with /setrules")
        break

# Set rules command
@Client.on_message(filters.command("setrules") & filters.group)
async def set_rules_handler(client: Client, message: Message):
    """Set group rules"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if len(message.command) > 1:
        rules_text = message.text.split(None, 1)[1]
    else:
        await message.reply("Usage: /setrules <rules text>")
        return
    
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            settings = ChatSettings(chat_id=chat_id, rules_text=rules_text)
            session.add(settings)
        else:
            settings.rules_text = rules_text
        
        await session.commit()
        await message.reply("✅ Rules updated!\n\n" + rules_text)
        break