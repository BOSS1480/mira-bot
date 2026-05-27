\"""
Notes handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Notes, get_session
from sqlalchemy import select, delete
import time

# Note command - get a note
@Client.on_message(filters.command("note") & filters.group)
async def note_handler(client: Client, message: Message):
    """Get a note"""
    chat_id = message.chat.id
    
    if len(message.command) > 1:
        note_name = message.command[1]
    else:
        await message.reply("Usage: /note <name>")
        return
    
    async for session in get_session():
        result = await session.execute(
            select(Notes).where(
                Notes.chat_id == chat_id,
                Notes.name == note_name
            )
        )
        note = result.scalar_one_or_none()
        
        if note:
            await message.reply(note.content)
        else:
            await message.reply(f"Note '{note_name}' not found!")
        break

# Add note command
@Client.on_message(filters.command("addnote") & filters.group)
async def add_note_handler(client: Client, message: Message):
    """Add a note"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    # Parse: /addnote <name> <content>
    if len(message.command) > 2:
        note_name = message.command[1]
        content = message.text.split(None, 2)[2]
    else:
        await message.reply("Usage: /addnote <name> <content>")
        return
    
    async for session in get_session():
        # Check if note exists
        result = await session.execute(
            select(Notes).where(
                Notes.chat_id == chat_id,
                Notes.name == note_name
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.content = content
        else:
            new_note = Notes(chat_id=chat_id, name=note_name, content=content)
            session.add(new_note)
        
        await session.commit()
        await message.reply(f"✅ Note '{note_name}' saved!")
        break

# Remove note command
@Client.on_message(filters.command("rmnote") & filters.group)
async def rm_note_handler(client: Client, message: Message):
    """Remove a note"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if len(message.command) > 1:
        note_name = message.command[1]
    else:
        await message.reply("Usage: /rmnote <name>")
        return
    
    async for session in get_session():
        await session.execute(
            delete(Notes).where(
                Notes.chat_id == chat_id,
                Notes.name == note_name
            )
        )
        await session.commit()
        await message.reply(f"✅ Note '{note_name}' removed!")
        break

# List notes command
@Client.on_message(filters.command("notes") & filters.group)
async def list_notes_handler(client: Client, message: Message):
    """List all notes"""
    chat_id = message.chat.id
    
    async for session in get_session():
        result = await session.execute(
            select(Notes).where(Notes.chat_id == chat_id)
        )
        notes = result.scalars().all()
        
        if notes:
            text = "📝 Notes:\n\n"
            for n in notes:
                text += f"• {n.name}\n"
            await message.reply(text)
        else:
            await message.reply("No notes saved!")
        break