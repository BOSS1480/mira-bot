\"""
Staff handlers - promote/demote
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Staff, get_session
from sqlalchemy import select, delete


# Promote command
@Client.on_message(filters.command("promote") & filters.group)
async def promote_handler(client: Client, message: Message):
    """Promote a user to admin"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name or "User"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user_name = "User"
        except:
            await message.reply("Invalid user ID")
            return
    else:
        await message.reply("Reply to a user or provide user ID")
        return
    
    try:
        await client.promote_chat_member(
            chat_id,
            user_id,
            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True
        )
        
        # Save to database
        async for session in get_session():
            result = await session.execute(
                select(Staff).where(
                    Staff.chat_id == chat_id,
                    Staff.user_id == user_id
                )
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                new_staff = Staff(chat_id=chat_id, user_id=user_id, rank="admin")
                session.add(new_staff)
                await session.commit()
        
        await message.reply(f"✅ {user_name} promoted to admin!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Demote command
@Client.on_message(filters.command("demote") & filters.group)
async def demote_handler(client: Client, message: Message):
    """Demote an admin"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name or "User"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user_name = "User"
        except:
            await message.reply("Invalid user ID")
            return
    else:
        await message.reply("Reply to a user or provide user ID")
        return
    
    try:
        await client.promote_chat_member(
            chat_id,
            user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False
        )
        
        # Remove from database
        async for session in get_session():
            await session.execute(
                delete(Staff).where(
                    Staff.chat_id == chat_id,
                    Staff.user_id == user_id
                )
            )
            await session.commit()
        
        await message.reply(f"✅ {user_name} demoted!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Staff command
@Client.on_message(filters.command("staff") & filters.group)
async def staff_handler(client: Client, message: Message):
    """List staff members"""
    chat_id = message.chat.id
    
    try:
        # Get admins from Telegram
        admins = await client.get_chat_members(chat_id, filter="administrators")
        
        if admins:
            text = "👮 Staff:\n\n"
            for member in admins:
                user = member.user
                name = user.first_name or "Unknown"
                if user.username:
                    name += f" (@{user.username})"
                text += f"• {name}\n"
            await message.reply(text)
        else:
            await message.reply("No staff found!")
    except Exception as e:
        await message.reply(f"Error: {e}")