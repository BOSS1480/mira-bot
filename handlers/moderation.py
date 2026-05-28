"""
Moderation handlers - ban, mute, kick, warn, purge, report
"""
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from sqlalchemy import select
from database import ChatSettings, UserWarnings, get_session
import asyncio
import time
from utils import tr, get_lang

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
        await message.reply(await tr(chat_id, "only_admins"))
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name or "User"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user_name = "User"
        except:
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    if await is_admin(chat_id, user_id, client):
        await message.reply(await tr(chat_id, "cannot_ban_admin"))
        return
    
    try:
        await client.ban_chat_member(chat_id, user_id)
        await message.reply(await tr(chat_id, "banned", name=user_name))
    except Exception as e:
        await message.reply(await tr(chat_id, "error", error=str(e)))

# Unban command
@Client.on_message(filters.command("unban") & filters.group)
async def unban_handler(client: Client, message: Message):
    """Unban a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply(await tr(chat_id, "only_admins"))
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    try:
        await client.unban_chat_member(chat_id, user_id)
        await message.reply(await tr(chat_id, "unbanned"))
    except Exception as e:
        await message.reply(await tr(chat_id, "error", error=str(e)))

# Mute command
@Client.on_message(filters.command("mute") & filters.group)
async def mute_handler(client: Client, message: Message):
    """Mute a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply(await tr(chat_id, "only_admins"))
        return
    
    duration = 60
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
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    try:
        until_date = int(time.time()) + (duration * 60)
        await client.restrict_chat_member(
            chat_id, user_id,
            ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.reply(await tr(chat_id, "muted", name=user_name, minutes=duration))
    except Exception as e:
        await message.reply(await tr(chat_id, "error", error=str(e)))

# Unmute command
@Client.on_message(filters.command("unmute") & filters.group)
async def unmute_handler(client: Client, message: Message):
    """Unmute a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply(await tr(chat_id, "only_admins"))
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    try:
        await client.restrict_chat_member(
            chat_id, user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply(await tr(chat_id, "unmuted"))
    except Exception as e:
        await message.reply(await tr(chat_id, "error", error=str(e)))

# Kick command
@Client.on_message(filters.command("kick") & filters.group)
async def kick_handler(client: Client, message: Message):
    """Kick a user from the group"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply(await tr(chat_id, "only_admins"))
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name or "User"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user_name = "User"
        except:
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    try:
        await client.ban_chat_member(chat_id, user_id)
        await client.unban_chat_member(chat_id, user_id)
        await message.reply(await tr(chat_id, "kicked", name=user_name))
    except Exception as e:
        await message.reply(await tr(chat_id, "error", error=str(e)))

# Warn command
@Client.on_message(filters.command("warn") & filters.group)
async def warn_handler(client: Client, message: Message):
    """Warn a user"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply(await tr(chat_id, "only_admins"))
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
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    async for session in get_session():
        warning = UserWarnings(
            chat_id=chat_id,
            user_id=user_id,
            reason=reason,
            timestamp=time.time()
        )
        session.add(warning)
        await session.commit()
        
        result = await session.execute(
            select(UserWarnings).where(
                UserWarnings.chat_id == chat_id,
                UserWarnings.user_id == user_id
            )
        )
        warn_count = len(result.scalars().all())
        
        settings = await get_chat_settings(chat_id)
        max_warns = 3
        
        if warn_count >= max_warns:
            try:
                await client.ban_chat_member(chat_id, user_id)
                await message.reply(
                    await tr(chat_id, "max_warnings", name=user_name, max=max_warns)
                )
            except:
                await message.reply(
                    await tr(chat_id, "warned", name=user_name, current=warn_count, max=max_warns, reason=reason)
                )
        else:
            await message.reply(
                await tr(chat_id, "warned", name=user_name, current=warn_count, max=max_warns, reason=reason)
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
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    async for session in get_session():
        result = await session.execute(
            select(UserWarnings).where(
                UserWarnings.chat_id == chat_id,
                UserWarnings.user_id == user_id
            )
        )
        warnings = result.scalars().all()
        warn_count = len(warnings)
        
        if warn_count == 0:
            await message.reply(await tr(chat_id, "no_warnings", name=user_name))
        else:
            text = ""
            for w in warnings:
                text += f"• {w.reason}\n"
            await message.reply(
                await tr(chat_id, "warnings_list", name=user_name, text=text, current=warn_count, max=3)
            )
        break

# Clearwarnings command
@Client.on_message(filters.command("clearwarnings") & filters.group)
async def clearwarnings_handler(client: Client, message: Message):
    """Clear user warnings"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply(await tr(chat_id, "only_admins"))
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name or "User"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user_name = "User"
        except:
            await message.reply(await tr(chat_id, "invalid_user"))
            return
    else:
        await message.reply(await tr(chat_id, "reply_or_id"))
        return
    
    async for session in get_session():
        await session.execute(
            UserWarnings.__table__.delete().where(
                UserWarnings.chat_id == chat_id,
                UserWarnings.user_id == user_id
            )
        )
        await session.commit()
        await message.reply(await tr(chat_id, "clearwarnings_done", name=user_name))
        break

# Purge command
@Client.on_message(filters.command("purge") & filters.group)
async def purge_handler(client: Client, message: Message):
    """Delete messages from replied message"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply(await tr(chat_id, "only_admins"))
        return
    
    if not message.reply_to_message:
        await message.reply(await tr(chat_id, "purge_reply"))
        return
    
    try:
        message_ids = list(range(message.reply_to_message.id, message.id))
        await client.delete_messages(chat_id, message_ids)
        await message.reply(await tr(chat_id, "purge_done", count=len(message_ids)))
    except Exception as e:
        await message.reply(await tr(chat_id, "error", error=str(e)))

# Report command
@Client.on_message(filters.command("report") & filters.group)
async def report_handler(client: Client, message: Message):
    """Report a user to admins"""
    if not message.from_user:
        return
    
    if not message.reply_to_message:
        await message.reply(await tr(message.chat.id, "report_reply"))
        return
    
    await message.reply(await tr(message.chat.id, "reported"))