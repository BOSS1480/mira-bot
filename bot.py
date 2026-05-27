#!/usr/bin/env python3
"""
Mira Bot - Telegram Group Management Bot
A MissRose-inspired bot with full moderation features
"""

import os
import sys
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, Chat, User, ChatMember
from pyrogram.errors import FloodWait, RPCError
from datetime import datetime

# Import local modules
from config import *
from database import db
from utils import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Pyrogram Client
app = Client(
    "mira_bot",
    bot_token=BOT_TOKEN,
    api_id=os.getenv("API_ID", ""),
    api_hash=os.getenv("API_HASH", ""),
    in_memory=True,
)

# ============== Basic Commands ==============

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    """Start command - Welcome message"""
    await message.reply_text(
        "**ברוך הבא ל-Mira Bot!** 🤖\n\n"
        "בוט לניהול קבוצות עם המון פיצ'רים!\n\n"
        "השתמש ב-`/help` כדי לראות את כל הפקודות.",
        quote=True
    )

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    """Help command - Show all commands"""
    help_text = """**📚 עזרה - פקודות זמינות**

**👤 פקודות בסיסיות:**
• /start - התחלת הבוט
• /help - תפריט עזרה
• /id - קבלת מזהים
• /info - מידע על משתמש
• /ping - בדיקת סטטוס הבוט

**👮 פקודות מנהלים:**
• /promote - העלאת משתמש למנהל
• /demote - הורדת מנהל
• /ban - חסימת משתמש
• /unban - ביטול חסימה
• /kick - הוצאת משתמש
• /mute - השתקת משתמש
• /unmute - ביטול השתקה
• /warn - אזהרה למשתמש
• /warns - הצגת אזהרות
• /clearwarns - ניקוי אזהרות
• /pin - נעילת הודעה
• /unpin - שחרור הודעה
• /purge - מחיקת הודעות

**🔒 נעילות:**
• /lock - נעילת פיצ'ר
• /unlock - פתיחת פיצ'ר
• /locks - הצגת כל הנעילות

**📝 הערות ומסננים:**
• /note - ניהול הערות
• /filter - ניהול מסננים
• /filters - הצגת מסננים

**📋 כללים וברכות:**
• /rules - הצגת כללים
• /setrules - קביעת כללים
• /welcome - קביעת ברכה

**⚙️ הגדרות:**
• /antiflood - הגדרות הגנה מהצפות
• /captcha - הגדרות CAPTCHA
• /setlang - שינוי שפה
• /settings - הגדרות הקבוצה

**🚫 רשימת חסימה:**
• /blocklist - הצגת רשימת חסימה
• /addblock - הוספת מילה לחסימה
• /unblock - הסרה מרשימת חסימה

**👥 צוות:**
• /staff - הצגת צוות
• /adminlist - רשימת מנהלים
"""
    
    # Check if user is admin in group
    if message.chat.type in ["group", "supergroup"]:
        if is_staff(message.from_user.id, message.chat.id, client):
            help_text += """
**🔧 פקודות צוות נוספות:**
• /grouplock - נעילת הקבוצה
• /groupunlock - פתיחת הקבוצה
• /setstaff - הגדרת תפקיד
• /connect - חיבור לקבוצה
"""
    
    await message.reply_text(help_text, quote=True)

@app.on_message(filters.command("id"))
async def id_command(client, message: Message):
    """Get IDs"""
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        chat = message.chat
        text = f"**מזהה משתמש:** `{user.id}`\n"
        text += f"**מזהה קבוצה:** `{chat.id}`"
        if message.reply_to_message.forward_from:
            text += f"\n**מזהה מקור:** `{message.reply_to_message.forward_from.id}`"
    else:
        text = f"**מזהה משתמש:** `{message.from_user.id}`\n"
        text += f"**מזהה קבוצה:** `{message.chat.id}`"
    
    await message.reply_text(text, quote=True)

@app.on_message(filters.command("info"))
async def info_command(client, message: Message):
    """Get user or chat info"""
    user = None
    chat = message.chat
    
    # Check if replying to a message
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        # Try to get user by username or ID
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text("משתמש לא נמצא!", quote=True)
            return
    else:
        user = message.from_user
    
    if user:
        text = f"**מידע על המשתמש:**\n\n"
        text += f"**ID:** `{user.id}`\n"
        if user.first_name:
            text += f"**שם:** {user.first_name}\n"
        if user.last_name:
            text += f"**שם משפחה:** {user.last_name}\n"
        if user.username:
            text += f"**יוזרניים:** @{user.username}\n"
        if user.is_verified:
            text += "**מאומת:** ✓\n"
        if user.is_premium:
            text += "**פרימיום:** ✓\n"
        if user.is_bot:
            text += "**בוט:** ✓\n"
    
    await message.reply_text(text, quote=True)

@app.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    """Ping - Check bot status"""
    start = datetime.now()
    msg = await message.reply_text("🏓 Pong!", quote=True)
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await msg.edit_text(f"🏓 Pong!\n`{ms}ms`")

# ============== Admin Commands ==============

@app.on_message(filters.command("promote") & filters.group)
async def promote_command(client, message: Message):
    """Promote user to admin"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_manage_video_chat=True,
        )
        await message.reply_text(
            tr("promoted", message.chat.id, user=get_user_mention(user), rank="מנהל"),
            quote=True
        )
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("demote") & filters.group)
async def demote_command(client, message: Message):
    """Demote user from admin"""
    if not is_owner(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_video_chat=False,
        )
        await message.reply_text(
            tr("demoted", message.chat.id, user=get_user_mention(user), rank="מנהל"),
            quote=True
        )
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("ban") & filters.group)
async def ban_command(client, message: Message):
    """Ban user from group"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    reason = extract_reason(" ".join(message.command[2:]))
    
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply_text(
            tr("banned", message.chat.id, user=get_user_mention(user)),
            quote=True
        )
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("unban") & filters.group)
async def unban_command(client, message: Message):
    """Unban user from group"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply_text(
            tr("unbanned", message.chat.id, user=get_user_mention(user)),
            quote=True
        )
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("kick") & filters.group)
async def kick_command(client, message: Message):
    """Kick user from group"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply_text(
            tr("kicked", message.chat.id, user=get_user_mention(user)),
            quote=True
        )
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("mute") & filters.group)
async def mute_command(client, message: Message):
    """Mute user"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    # Parse time
    time_seconds = 60 * 60 * 24 * 365  # Default: 1 year
    if len(message.command) > 2:
        time_seconds = parse_time(message.command[2]) or time_seconds
    
    try:
        await client.restrict_chat_member(
            message.chat.id,
            user.id,
            until_date=datetime.now() + timedelta(seconds=time_seconds),
            can_send_messages=False,
        )
        await message.reply_text(
            tr("muted", message.chat.id, user=get_user_mention(user), time=format_time(time_seconds)),
            quote=True
        )
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("unmute") & filters.group)
async def unmute_command(client, message: Message):
    """Unmute user"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    try:
        await client.restrict_chat_member(
            message.chat.id,
            user.id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        await message.reply_text(
            tr("unmuted", message.chat.id, user=get_user_mention(user)),
            quote=True
        )
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

# ============== Warning Commands ==============

@app.on_message(filters.command("warn") & filters.group)
async def warn_command(client, message: Message):
    """Warn user"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    reason = extract_reason(" ".join(message.command[2:]))
    
    # Add warn to database
    db.add_warn(user.id, message.chat.id, reason, message.from_user.id)
    
    # Get warns count
    warns_count = db.get_warns(user.id, message.chat.id)
    group = db.get_group(message.chat.id)
    max_warns = group.get("warns_limit", 3) if group else 3
    
    await message.reply_text(
        tr("warned", message.chat.id, 
           user=get_user_mention(user), 
           reason=reason, 
           count=warns_count, 
           max=max_warns),
        quote=True
    )
    
    # Check if max warns reached
    if warns_count >= max_warns:
        try:
            await client.ban_chat_member(message.chat.id, user.id)
            await message.reply_text(
                f"{get_user_mention(user)} חסם בגלל שהגיע למקסימום אזהרות!",
                quote=True
            )
        except:
            pass

@app.on_message(filters.command("warns") & filters.group)
async def warns_command(client, message: Message):
    """Get user warns"""
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    else:
        user = message.from_user
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    warns_count = db.get_warns(user.id, message.chat.id)
    warn_history = db.get_warn_history(user.id, message.chat.id)
    
    text = f"**אזהרות של {get_user_mention(user)}:**\n\n"
    text += f"**סה"כ:** {warns_count}\n\n"
    
    if warn_history:
        text += "**היסטוריה:**\n"
        for i, warn in enumerate(warn_history, 1):
            text += f"{i}. {warn['reason']}\n"
    
    await message.reply_text(text, quote=True)

@app.on_message(filters.command("clearwarns") & filters.group)
async def clearwarns_command(client, message: Message):
    """Clear user warns"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
            return
    
    if not user:
        await message.reply_text(tr("user_not_found", message.chat.id), quote=True)
        return
    
    db.clear_warns(user.id, message.chat.id)
    
    await message.reply_text(
        tr("warns_cleared", message.chat.id, user=get_user_mention(user)),
        quote=True
    )

# ============== Pin/Unpin Commands ==============


@app.on_message(filters.command("pin") & filters.group)
async def pin_command(client, message: Message):
    """Pin message"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if not message.reply_to_message:
        await message.reply_text("ענה על הודעה כדי לנעוץ אותה!", quote=True)
        return
    
    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.id)
        await message.reply_text(tr("pinned", message.chat.id), quote=True)
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("unpin") & filters.group)
async def unpin_command(client, message: Message):
    """Unpin message"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    try:
        await client.unpin_chat_message(message.chat.id)
        await message.reply_text(tr("unpinned", message.chat.id), quote=True)
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("purge") & filters.group)
async def purge_command(client, message: Message):
    """Delete messages"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if not message.reply_to_message:
        await message.reply_text("ענה על הודעה כדי למחוק אותה ואת הבאות!", quote=True)
        return
    
    try:
        message_id = message.reply_to_message.id
        deleted = 0
        
        for msg_id in range(message_id, message.message_id + 1):
            try:
                await client.delete_messages(message.chat.id, msg_id)
                deleted += 1
            except:
                pass
        
        await message.reply_text(tr("deleted", message.chat.id), quote=True)
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

# ============== Lock/Unlock Commands ==============

LOCK_TYPES = [
    "stickers", "photos", "videos", "documents", "games",
    "inline", "polls", "voice", "videochat", "location",
    "contacts", "rtl", "button", "eggs"
]

@app.on_message(filters.command("lock") & filters.group)
async def lock_command(client, message: Message):
    """Lock a feature"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        text = "**סוגי נעילה זמינים:**\n\n"
        for lock in LOCK_TYPES:
            text += f"• `{lock}`\n"
        await message.reply_text(text, quote=True)
        return
    
    lock_type = message.command[1].lower()
    if lock_type not in LOCK_TYPES:
        await message.reply_text(f"סוג נעילה לא מוכר: {lock_type}", quote=True)
        return
    
    # Update group locks
    group = db.get_group(message.chat.id)
    if group:
        locks = group.get("locks", {})
        locks[lock_type] = True
        db.update_group(message.chat.id, locks=locks)
    
    await message.reply_text(
        tr("lock_enabled", message.chat.id, item=lock_type),
        quote=True
    )

@app.on_message(filters.command("unlock") & filters.group)
async def unlock_command(client, message: Message):
    """Unlock a feature"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        text = "**סוגי נעילה זמינים:**\n\n"
        for lock in LOCK_TYPES:
            text += f"• `{lock}`\n"
        await message.reply_text(text, quote=True)
        return
    
    lock_type = message.command[1].lower()
    if lock_type not in LOCK_TYPES:
        await message.reply_text(f"סוג נעילה לא מוכר: {lock_type}", quote=True)
        return
    
    # Update group locks
    group = db.get_group(message.chat.id)
    if group:
        locks = group.get("locks", {})
        locks[lock_type] = False
        db.update_group(message.chat.id, locks=locks)
    
    await message.reply_text(
        tr("lock_disabled", message.chat.id, item=lock_type),
        quote=True
    )

@app.on_message(filters.command("locks") & filters.group)
async def locks_command(client, message: Message):
    """Show all locks"""
    group = db.get_group(message.chat.id)
    
    text = "**נעילות בקבוצה:**\n\n"
    
    if group:
        locks = group.get("locks", {})
        for lock in LOCK_TYPES:
            status = "🔒" if locks.get(lock, False) else "🔓"
            text += f"{status} {lock}\n"
    else:
        for lock in LOCK_TYPES:
            text += f"🔓 {lock}\n"
    
    await message.reply_text(text, quote=True)

# ============== Rules Commands ==============

@app.on_message(filters.command("rules") & filters.group)
async def rules_command(client, message: Message):
    """Show group rules"""
    group = db.get_group(message.chat.id)
    
    if group and group.get("rules"):
        await message.reply_text(
            tr("rules", message.chat.id, rules=group["rules"]),
            quote=True
        )
    else:
        await message.reply_text(
            tr("no_rules", message.chat.id),
            quote=True
        )

@app.on_message(filters.command("setrules") & filters.group)
async def setrules_command(client, message: Message):
    """Set group rules"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("השתמש ב-`/setrules <כללים>` כדי לקבוע כללים!", quote=True)
        return
    
    rules = " ".join(message.command[1:])
    if message.reply_to_message:
        rules = message.reply_to_message.text or message.reply_to_message.caption or ""
    
    # Update group rules
    db.update_group(message.chat.id, rules=rules)
    
    await message.reply_text(tr("rules_set", message.chat.id), quote=True)

# ============== Welcome Commands ==============

@app.on_message(filters.command("welcome") & filters.group)
async def welcome_command(client, message: Message):
    """Set welcome message"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2 and not message.reply_to_message:
        # Show current welcome
        group = db.get_group(message.chat.id)
        if group and group.get("welcome"):
            await message.reply_text(
                f"**ברכה נוכחית:**\n{group['welcome']}",
                quote=True
            )
        else:
            await message.reply_text(
                "השתמש ב-`/welcome <הודעה>` כדי לקבוע ברכה!\n\n"
                "ניתן להשתמש ב-`{first}` לשם המשתמש ו-`{group}` לשם הקבוצה.",
                quote=True
            )
        return
    
    welcome = " ".join(message.command[1:])
    if message.reply_to_message:
        welcome = message.reply_to_message.text or message.reply_to_message.caption or ""
    
    # Update group welcome
    db.update_group(message.chat.id, welcome=welcome, welcome_enabled=1)
    
    await message.reply_text(tr("welcome_set", message.chat.id), quote=True)

# ============== Notes Commands ==============

@app.on_message(filters.command("note") & filters.group)
async def note_command(client, message: Message):
    """Manage notes"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        # List notes
        notes = db.get_notes(message.chat.id)
        if notes:
            text = "**הערות בקבוצה:**\n\n"
            for note in notes:
                text += f"• `{note['name']}`\n"
        else:
            text = tr("no_notes", message.chat.id)
        await message.reply_text(text, quote=True)
        return
    
    action = message.command[1].lower()
    
    if action == "add":
        if len(message.command) < 4:
            await message.reply_text("השתמש ב-`/note add <שם> <תוכן>`!", quote=True)
            return
        name = message.command[2]
        content = " ".join(message.command[3:])
        
        if message.reply_to_message:
            content = message.reply_to_message.text or message.reply_to_message.caption or ""
        
        db.add_note(message.chat.id, name, content, get_file_id(message.reply_to_message), message.from_user.id)
        await message.reply_text(tr("note_added", message.chat.id), quote=True)
    
    elif action == "del" or action == "delete" or action == "remove":
        if len(message.command) < 3:
            await message.reply_text("השתמש ב-`/note del <שם>`!", quote=True)
            return
        name = message.command[2]
        db.delete_note(message.chat.id, name)
        await message.reply_text(tr("note_removed", message.chat.id), quote=True)
    
    else:
        # Get note
        name = message.command[1]
        note = db.get_note(message.chat.id, name)
        if note:
            if note.get("file_id"):
                await message.reply_cached_media(note["file_id"], quote=True)
            else:
                await message.reply_text(note["content"], quote=True)
        else:
            await message.reply_text("הערה לא נמצאה!", quote=True)

# ============== Filters Commands ==============


@app.on_message(filters.command("filter") & filters.group)
async def filter_command(client, message: Message):
    """Manage filters"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        # List filters
        filters_list = db.get_filters(message.chat.id)
        if filters_list:
            text = "**מסננים בקבוצה:**\n\n"
            for f in filters_list:
                text += f"• `{f['keyword']}` → {f['response'][:50]}...\n"
        else:
            text = tr("no_filters", message.chat.id)
        await message.reply_text(text, quote=True)
        return
    
    action = message.command[1].lower()
    
    if action == "add":
        if len(message.command) < 4:
            await message.reply_text("השתמש ב-`/filter add <מילה> <תגובה>`!", quote=True)
            return
        keyword = message.command[2]
        response = " ".join(message.command[3:])
        
        if message.reply_to_message:
            response = message.reply_to_message.text or message.reply_to_message.caption or ""
        
        db.add_filter(message.chat.id, keyword, response, get_file_id(message.reply_to_message), message.from_user.id)
        await message.reply_text(tr("filter_added", message.chat.id), quote=True)
    
    elif action == "del" or action == "delete" or action == "remove":
        if len(message.command) < 3:
            await message.reply_text("השתמש ב-`/filter del <מילה>`!", quote=True)
            return
        keyword = message.command[2]
        db.delete_filter(message.chat.id, keyword)
        await message.reply_text(tr("filter_removed", message.chat.id), quote=True)

@app.on_message(filters.command("filters") & filters.group)
async def filters_command(client, message: Message):
    """List all filters"""
    filters_list = db.get_filters(message.chat.id)
    
    if filters_list:
        text = "**מסננים בקבוצה:**\n\n"
        for f in filters_list:
            text += f"• `{f['keyword']}` → {f['response'][:50]}\n"
    else:
        text = tr("no_filters", message.chat.id)
    
    await message.reply_text(text, quote=True)

# ============== Anti-Flood Commands ==============

@app.on_message(filters.command("antiflood") & filters.group)
async def antiflood_command(client, message: Message):
    """Manage anti-flood"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        # Show current settings
        group = db.get_group(message.chat.id)
        if group and group.get("antiflood"):
            await message.reply_text(
                f"**הגנה מפני הצפות:** הופעלה\n"
                f"**מגבלת הודעות:** {group.get('flood_limit', 5)}",
                quote=True
            )
        else:
            await message.reply_text(
                "**הגנה מפני הצפות:** כבויה\n\n"
                "השתמש ב-`/antiflood set <מספר>` כדי להפעיל!",
                quote=True
            )
        return
    
    action = message.command[1].lower()
    
    if action == "set":
        limit = int(message.command[2]) if len(message.command) > 2 else 5
        db.update_group(message.chat.id, antiflood=1, flood_limit=limit)
        await message.reply_text(tr("antiflood_enabled", message.chat.id), quote=True)
    
    elif action == "del" or action == "off":
        db.update_group(message.chat.id, antiflood=0)
        await message.reply_text(tr("antiflood_disabled", message.chat.id), quote=True)

# ============== Language Commands ==============

@app.on_message(filters.command("setlang") & filters.group)
async def setlang_command(client, message: Message):
    """Set group language"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        await message.reply_text(
            f"**שפות זמינות:**\n\n{get_language_list()}\n\n"
            "השתמש ב-`/setlang <קוד>` כדי לשנות שפה!",
            quote=True
        )
        return
    
    lang = message.command[1].lower()
    if not get_language(lang):
        await message.reply_text("שפה לא מוכרת!", quote=True)
        return
    
    db.update_group(message.chat.id, language=lang)
    await message.reply_text(
        tr("language_set", message.chat.id, lang=get_language(lang)["name"]),
        quote=True
    )

# ============== Blocklist Commands ==============


@app.on_message(filters.command("blocklist") & filters.group)
async def blocklist_command(client, message: Message):
    """Show blocklist"""
    group = db.get_group(message.chat.id)
    
    if group:
        blocklist = group.get("blocklist", [])
        if blocklist:
            text = "**רשימת חסימה:**\n\n"
            for word in blocklist:
                text += f"• `{word}`\n"
        else:
            text = tr("no_blocklist", message.chat.id)
    else:
        text = tr("no_blocklist", message.chat.id)
    
    await message.reply_text(text, quote=True)

@app.on_message(filters.command("addblock") & filters.group)
async def addblock_command(client, message: Message):
    """Add word to blocklist"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        await message.reply_text("השתמש ב-`/addblock <מילה>`!", quote=True)
        return
    
    word = message.command[1].lower()
    
    group = db.get_group(message.chat.id)
    if group:
        blocklist = group.get("blocklist", [])
        if word not in blocklist:
            blocklist.append(word)
            db.update_group(message.chat.id, blocklist=blocklist)
    else:
        db.update_group(message.chat.id, blocklist=[word])
    
    await message.reply_text(
        tr("blocklist_added", message.chat.id, word=word),
        quote=True
    )

@app.on_message(filters.command("unblock") & filters.group)
async def unblock_command(client, message: Message):
    """Remove word from blocklist"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        await message.reply_text("השתמש ב-`/unblock <מילה>`!", quote=True)
        return
    
    word = message.command[1].lower()
    
    group = db.get_group(message.chat.id)
    if group:
        blocklist = group.get("blocklist", [])
        if word in blocklist:
            blocklist.remove(word)
            db.update_group(message.chat.id, blocklist=blocklist)
    
    await message.reply_text(
        tr("blocklist_removed", message.chat.id, word=word),
        quote=True
    )

# ============== Staff Commands ==============


@app.on_message(filters.command("staff") & filters.group)
async def staff_command(client, message: Message):
    """Show staff list"""
    try:
        admins = await client.get_chat_administrators(message.chat.id)
        
        text = "**👥 צוות הקבוצה:**\n\n"
        
        for admin in admins:
            user = admin.user
            status = "👑" if admin.status == "creator" else "👮"
            name = user.first_name or "Unknown"
            if user.username:
                name = f"@{user.username}"
            text += f"{status} {name}\n"
        
        await message.reply_text(text, quote=True)
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("adminlist") & filters.group)
async def adminlist_command(client, message: Message):
    """Show admin list (alias for staff)"""
    await staff_command(client, message)

# ============== Group Lock Commands ==============


@app.on_message(filters.command("grouplock") & filters.group)
async def grouplock_command(client, message: Message):
    """Lock entire group"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    try:
        # Lock all
        for lock_type in LOCK_TYPES:
            group = db.get_group(message.chat.id)
            if group:
                locks = group.get("locks", {})
                locks[lock_type] = True
                db.update_group(message.chat.id, locks=locks)
        
        await message.reply_text("🔒 הקבוצה ננעלה!", quote=True)
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

@app.on_message(filters.command("groupunlock") & filters.group)
async def groupunlock_command(client, message: Message):
    """Unlock entire group"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    try:
        # Unlock all
        for lock_type in LOCK_TYPES:
            group = db.get_group(message.chat.id)
            if group:
                locks = group.get("locks", {})
                locks[lock_type] = False
                db.update_group(message.chat.id, locks=locks)
        
        await message.reply_text("🔓 הקבוצה נפתחה!", quote=True)
    except RPCError as e:
        await message.reply_text(f"שגיאה: {e}", quote=True)

# ============== Settings Command ==============

@app.on_message(filters.command("settings") & filters.group)
async def settings_command(client, message: Message):
    """Show group settings"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    group = db.get_group(message.chat.id)
    
    text = "**⚙️ הגדרות הקבוצה:**\n\n"
    
    if group:
        text += f"**שפה:** {group.get('language', 'he')}\n"
        text += f"**ברכה:** {'✓' if group.get('welcome_enabled') else '✗'}\n"
        text += f"**הגנה מהצפות:** {'✓' if group.get('antiflood') else '✗'}\n"
        text += f"**CAPTCHA:** {'✓' if group.get('captcha') else '✗'}\n"
        text += f"**מגבלת אזהרות:** {group.get('warns_limit', 3)}\n"
    else:
        text += "**שפה:** he\n"
        text += "**ברכה:** ✓\n"
        text += "**הגנה מהצפות:** ✗\n"
        text += "**CAPTCHA:** ✗\n"
        text += "**מגבלת אזהרות:** 3\n"
    
    await message.reply_text(text, quote=True)

# ============== CAPTCHA Commands ==============


@app.on_message(filters.command("captcha") & filters.group)
async def captcha_command(client, message: Message):
    """Manage CAPTCHA"""
    if not is_staff(message.from_user.id, message.chat.id, client):
        await message.reply_text(tr("no_permission", message.chat.id), quote=True)
        return
    
    if len(message.command) < 2:
        group = db.get_group(message.chat.id)
        if group and group.get("captcha"):
            await message.reply_text(
                f"**CAPTCHA:** הופעל\n**זמן:** {group.get('captcha_time', 60)} שניות",
                quote=True
            )
        else:
            await message.reply_text(
                "**CAPTCHA:** כבוי\n\n"
                "השתמש ב-`/captcha on` כדי להפעיל!",
                quote=True
            )
        return
    
    action = message.command[1].lower()
    
    if action == "on" or action == "set":
        db.update_group(message.chat.id, captcha=1, captcha_time=60)
        await message.reply_text(tr("captcha_enabled", message.chat.id), quote=True)
    
    elif action == "off" or action == "del":
        db.update_group(message.chat.id, captcha=0)
        await message.reply_text(tr("captcha_disabled", message.chat.id), quote=True)

# ============== Message Handlers ==============


@app.on_message(filters.new_chat_members)
async def new_members_handler(client, message: Message):
    """Handle new members joining"""
    if not message.new_chat_members:
        return
    
    for member in message.new_chat_members:
        # Skip if bot
        if member.is_bot:
            continue
        
        # Add user to database
        db.add_user(member.id, member.first_name, member.last_name, member.username)
        
        # Check CAPTCHA
        group = db.get_group(message.chat.id)
        if group and group.get("captcha"):
            # TODO: Implement CAPTCHA verification
            pass
        
        # Send welcome message
        if group and group.get("welcome_enabled") and group.get("welcome"):
            welcome_text = group["welcome"]
            welcome_text = welcome_text.replace("{first}", member.first_name or "User")
            welcome_text = welcome_text.replace("{group}", message.chat.title or "this group")
            welcome_text = welcome_text.replace("{fullname}", f"{member.first_name or ''} {member.last_name or ''}".strip())
            welcome_text = welcome_text.replace("{username}", f"@{member.username}" if member.username else "No username")
            
            await message.reply_text(welcome_text)
        else:
            # Default welcome
            await message.reply_text(
                f"ברוך הבא {member.first_name or 'User'}! 👋"
            )

@app.on_message(filters.left_chat_member)
async def left_member_handler(client, message: Message):
    """Handle member leaving"""
    if not message.left_chat_member:
        return
    
    member = message.left_chat_member
    
    if member.is_bot:
        return
    
    # Send goodbye message
    group = db.get_group(message.chat.id)
    if group and group.get("welcome_enabled"):
        await message.reply_text(
            f"להתראות {member.first_name or 'User'}! נשמח לראותך שוב 😢"
        )


# ============== Filter Handler ==============


@app.on_message(filters.group & filters.text)
async def filter_handler(client, message: Message):
    """Handle filters"""
    if not message.text:
        return
    
    text = message.text.lower()
    
    # Check filters
    filters_list = db.get_filters(message.chat.id)
    for f in filters_list:
        if f['keyword'].lower() in text:
            await message.reply_text(f['response'])
            return

# ============== Blocklist Handler ==============

@app.on_message(filters.group & filters.text)
async def blocklist_handler(client, message: Message):
    """Handle blocklist"""
    if not message.text:
        return
    
    text = message.text.lower()
    
    # Check blocklist
    group = db.get_group(message.chat.id)
    if group:
        blocklist = group.get("blocklist", [])
        for word in blocklist:
            if word in text:
                try:
                    await message.delete()
                    await message.reply_text(
                        f"{message.from_user.mention}, ההודעה נמחקה בגלל מילה חסומה!",
                        quote=True
                    )
                except:
                    pass
                return


# ============== Anti-Flood Handler ==============

# Simple flood control - track message count per user
flood_data = {}

@app.on_message(filters.group)
async def antiflood_handler(client, message: Message):
    """Handle anti-flood"""
    if not message.from_user:
        return
    
    group = db.get_group(message.chat.id)
    if not group or not group.get("antiflood"):
        return
    
    user_id = message.from_user.id
    chat_id = message.chat.id
    flood_limit = group.get("flood_limit", 5)
    
    key = f"{chat_id}:{user_id}"
    
    if key not in flood_data:
        flood_data[key] = {"count": 0, "time": datetime.now()}
    
    # Check if time expired (reset count)
    elapsed = (datetime.now() - flood_data[key]["time"]).seconds
    if elapsed > 6:
        flood_data[key] = {"count": 0, "time": datetime.now()}
    
    flood_data[key]["count"] += 1
    
    if flood_data[key]["count"] > flood_limit:
        try:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                until_date=datetime.now(),
                can_send_messages=False,
            )
            await message.reply_text(
                f"{message.from_user.mention}, הושתקת בגלל הצפת הודעות!",
                quote=True
            )
            flood_data[key]["count"] = 0
        except:
            pass

# ============== Lock Handlers ==============

@app.on_message(filters.group & filters.sticker)
async def lock_sticker_handler(client, message: Message):
    """Handle sticker lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("stickers"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.photo)
async def lock_photo_handler(client, message: Message):
    """Handle photo lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("photos"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.video)
async def lock_video_handler(client, message: Message):
    """Handle video lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("videos"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.document)
async def lock_document_handler(client, message: Message):
    """Handle document lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("documents"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.game)
async def lock_game_handler(client, message: Message):
    """Handle game lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("games"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.inline_keyboard)
async def lock_inline_handler(client, message: Message):
    """Handle inline lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("inline"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.poll)
async def lock_poll_handler(client, message: Message):
    """Handle poll lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("polls"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.voice)
async def lock_voice_handler(client, message: Message):
    """Handle voice lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("voice"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.location)
async def lock_location_handler(client, message: Message):
    """Handle location lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("location"):
        try:
            await message.delete()
        except:
            pass

@app.on_message(filters.group & filters.contact)
async def lock_contact_handler(client, message: Message):
    """Handle contact lock"""
    group = db.get_group(message.chat.id)
    if group and group.get("locks", {}).get("contacts"):
        try:
            await message.delete()
        except:
            pass

# ============== Chat Join Request Handler ==============

@app.on_chat_join_request()
async def chat_join_request_handler(client, message: Message):
    """Handle join requests"""
    user = message.from_user
    chat = message.chat
    
    # Add user to database
    db.add_user(user.id, user.first_name, user.last_name, user.username)
    
    # Check if CAPTCHA is enabled
    group = db.get_group(chat.id)
    if group and group.get("captcha"):
        # TODO: Send CAPTCHA challenge
        pass

# ============== Error Handler ==============


@app.on_error()
async def error_handler(client, message: Message, error):
    """Handle errors"""
    logger.error(f"Error: {error}")
    print(f"Error: {error}")


# ============== Run Bot ==============


if __name__ == "__main__":
    print("🚀 Starting Mira Bot...")
    
    # Run the bot
    app.run()
    
    print("👋 Mira Bot Stopped")