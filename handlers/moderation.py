\"""
Moderation handlers - ban, mute, kick, warn, purge
"""
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from sqlalchemy import select, delete, func
from database import ChatSettings, UserWarnings, get_session
import asyncio
import time

# Helper to check if user is admin
async def is_admin(chat_id: int, user_id: int, app: Client) -> bool:
    """Check if user is admin in chat"""
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ["creator", "administrator"]
    except:
        return False

# Helper to get chat settings
async def get_chat_settings(chat_id: int):
    """Get or create chat settings"""
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        if not settings:
            settings = ChatSettings(chat_id=chat_id)
            session.add(settings)
            await session.commit()
        return settings

# Ban command
@Client.on_message(filters.command("ban") & filters.group)
async def ban_handler(client: Client, message: Message):
    """Ban a user from the group"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    # Get user to ban
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
    
    # Check if trying to ban admin
    if await is_admin(chat_id, user_id, client):
        await message.reply("Cannot ban an admin!")
        return
    
    try:
        await client.ban_chat_member(chat_id, user_id)
        await message.reply(f"🚫 Banned {user_name}!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Unban command
@Client.on_message(filters.command("unban") & filters.group)
async def unban_handler(client: Client, message: Message):
    """Unban a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply("Invalid user ID")
            return
    else:
        await message.reply("Reply to a user or provide user ID")
        return
    
    try:
        await client.unban_chat_member(chat_id, user_id)
        await message.reply("✅ User unbanned!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Mute command
@Client.on_message(filters.command("mute") & filters.group)
async def mute_handler(client: Client, message: Message):
    """Mute a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    # Parse duration
    duration = 60  # default 60 minutes
    if len(message.command) > 2:
        try:
            duration = int(message.command[2])
        except:
            pass
    
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
        until_date = int(time.time()) + (duration * 60)
        await client.restrict_chat_member(
            chat_id, user_id,
            ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.reply(f"🔇 Muted {user_name} for {duration} minutes!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Unmute command
@Client.on_message(filters.command("unmute") & filters.group)
async def unmute_handler(client: Client, message: Message):
    """Unmute a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply("Invalid user ID")
            return
    else:
        await message.reply("Reply to a user or provide user ID")
        return
    
    try:
        await client.restrict_chat_member(
            chat_id, user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_invite_users=True,
                can_pin_messages=True
            )
        )
        await message.reply("✅ User unmuted!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Kick command
@Client.on_message(filters.command("kick") & filters.group)
async def kick_handler(client: Client, message: Message):
    """Kick a user from the group"""
    if not message.from_user:
        return
    
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
        await client.ban_chat_member(chat_id, user_id)
        await client.unban_chat_member(chat_id, user_id)
        await message.reply(f"👢 Kicked {user_name}!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Warn command
@Client.on_message(filters.command("warn") & filters.group)
async def warn_handler(client: Client, message: Message):
    """Warn a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    reason = "No reason"
    if len(message.command) > 2:
        reason = " ".join(message.command[2:])
    
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
    
    # Save warning to database
    async for session in get_session():
        warning = UserWarnings(
            chat_id=chat_id,
            user_id=user_id,
            reason=reason,
            timestamp=time.time()
        )
        session.add(warning)
        await session.commit()
        
        # Count warnings
        result = await session.execute(
            select(UserWarnings).where(
                UserWarnings.chat_id == chat_id,
                UserWarnings.user_id == user_id
            )
        )
        warn_count = len(result.scalars().all())
        
        settings = await get_chat_settings(chat_id)
        max_warns = settings.max_warnings or 3
        
        if warn_count >= max_warns:
            # Ban the user
            try:
                await client.ban_chat_member(chat_id, user_id)
                await message.reply(
                    f"⚠️ {user_name} reached {max_warns} warnings and was banned!"
                )
            except:
                await message.reply(
                    f"⚠️ {user_name} has {warn_count}/{max_warns} warnings!"
                )
        else:
            await message.reply(
                f"⚠️ {user_name} warned! ({warn_count}/{max_warns})\nReason: {reason}"
            )
        break

# Warnings command
@Client.on_message(filters.command("warnings") & filters.group)
async def warnings_handler(client: Client, message: Message):
    """Check user warnings"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    
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
    
    async for session in get_session():
        result = await session.execute(
            select(UserWarnings).where(
                UserWarnings.chat_id == chat_id,
                UserWarnings.user_id == user_id
            )
        )
        warnings = result.scalars().all()
        
        if warnings:
            text = f"⚠️ Warnings for {user_name}:\n\n"
            for w in warnings:
                text += f"• {w.reason}\n"
            await message.reply(text)
        else:
            await message.reply(f"✅ {user_name} has no warnings!")
        break

# Clearwarnings command
@Client.on_message(filters.command("clearwarnings") & filters.group)
async def clearwarnings_handler(client: Client, message: Message):
    """Clear user warnings"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply("Invalid user ID")
            return
    else:
        await message.reply("Reply to a user or provide user ID")
        return
    
    async for session in get_session():
        await session.execute(
            delete(UserWarnings).where(
                UserWarnings.chat_id == chat_id,
                UserWarnings.user_id == user_id
            )
        )
        await session.commit()
        await message.reply("✅ Warnings cleared!")
        break

# Purge command (delete messages)
@Client.on_message(filters.command("purge") & filters.group)
async def purge_handler(client: Client, message: Message):
    """Delete messages from replied message"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if not message.reply_to_message:
        await message.reply("Reply to a message to delete from")
        return
    
    try:
        # Delete messages from replied to current
        message_ids = list(range(message.reply_to_message.id, message.id))
        await client.delete_messages(chat_id, message_ids)
        await message.reply(f"🗑️ Deleted {len(message_ids)} messages!")
    except Exception as e:
        await message.reply(f"Error: {e}")