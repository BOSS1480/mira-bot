\"""
Filters and blocklist handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Filters, Blocklist, ChatSettings, get_session
from sqlalchemy import select, delete

# Filter handler - respond to keywords
@Client.on_message(filters.group & filters.text)
async def filter_handler(client: Client, message: Message):
    """Check for filters and respond"""
    if not message.text:
        return
    
    chat_id = message.chat.id
    text = message.text.lower()
    
    # Check blocklist
    async for session in get_session():
        result = await session.execute(
            select(Blocklist).where(Blocklist.chat_id == chat_id)
        )
        blocklist = result.scalars().all()
        
        for blocked in blocklist:
            if blocked.word.lower() in text:
                try:
                    await message.delete()
                    return
                except:
                    pass
        
        # Check filters
        result = await session.execute(
            select(Filters).where(Filters.chat_id == chat_id)
        )
        filters_list = result.scalars().all()
        
        for f in filters_list:
            if f.keyword.lower() in text:
                await message.reply(f.response)
                break
        
        break


# Add filter command
@Client.on_message(filters.command("addfilter") & filters.group)
async def add_filter_handler(client: Client, message: Message):
    """Add a filter"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    # Parse: /addfilter <keyword> <response>
    if len(message.command) > 2:
        keyword = message.command[1]
        response = message.text.split(None, 2)[2]
    else:
        await message.reply("Usage: /addfilter <keyword> <response>")
        return
    
    async for session in get_session():
        new_filter = Filters(chat_id=chat_id, keyword=keyword, response=response)
        session.add(new_filter)
        await session.commit()
        await message.reply(f"✅ Filter added!\nKeyword: {keyword}\nResponse: {response}")
        break

# Remove filter command
@Client.on_message(filters.command("rmfilter") & filters.group)
async def rm_filter_handler(client: Client, message: Message):
    """Remove a filter"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if len(message.command) > 1:
        keyword = message.command[1]
    else:
        await message.reply("Usage: /rmfilter <keyword>")
        return
    
    async for session in get_session():
        await session.execute(
            delete(Filters).where(
                Filters.chat_id == chat_id,
                Filters.keyword == keyword
            )
        )
        await session.commit()
        await message.reply(f"✅ Filter '{keyword}' removed!")
        break

# List filters command
@Client.on_message(filters.command("listfilters") & filters.group)
async def list_filters_handler(client: Client, message: Message):
    """List all filters"""
    chat_id = message.chat.id
    
    async for session in get_session():
        result = await session.execute(
            select(Filters).where(Filters.chat_id == chat_id)
        )
        filters_list = result.scalars().all()
        
        if not filters_list:
            await message.reply("No filters set!")
        else:
            text = "📋 *Filters:*\n\n"
            for f in filters_list:
                text += f"• `{f.keyword}` → {f.response}\n"
            await message.reply(text)
        break

# Blocklist command
@Client.on_message(filters.command("blocklist") & filters.group)
async def blocklist_handler(client: Client, message: Message):
    """Manage blocklist"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    # Parse subcommand
    if len(message.command) > 2:
        subcmd = message.command[1]
        word = message.command[2]
    elif len(message.command) > 1:
        subcmd = message.command[1]
        word = None
    else:
        await message.reply("Usage: /blocklist add/remove <word>")
        return
    
    async for session in get_session():
        if subcmd == "add" and word:
            blocked = Blocklist(chat_id=chat_id, word=word)
            session.add(blocked)
            await session.commit()
            await message.reply(f"✅ Added '{word}' to blocklist!")
        elif subcmd == "remove" and word:
            await session.execute(
                delete(Blocklist).where(
                    Blocklist.chat_id == chat_id,
                    Blocklist.word == word
                )
            )
            await session.commit()
            await message.reply(f"✅ Removed '{word}' from blocklist!")
        elif subcmd == "list":
            result = await session.execute(
                select(Blocklist).where(Blocklist.chat_id == chat_id)
            )
            blocklist = result.scalars().all()
            if not blocklist:
                await message.reply("Blocklist is empty!")
            else:
                text = "🚫 *Blocklist:*\n\n"
                for b in blocklist:
                    text += f"• `{b.word}`\n"
                await message.reply(text)
        else:
            await message.reply("Usage: /blocklist add/remove/list <word>")
        break