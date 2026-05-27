import os
import re
import json
import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from functools import wraps
import asyncio

# ============== Helper Functions ==============

def get_id_from_command(command: str) -> Optional[int]:
    """Extract ID from command arguments"""
    match = re.search(r'\d+', command)
    return int(match.group()) if match else None

def extract_reason(text: str, max_length: int = 100) -> str:
    """Extract reason from text"""
    if not text:
        return "No reason"
    reason = text.strip()
    if len(reason) > max_length:
        reason = reason[:max_length] + "..."
    return reason

def escape_html(text: str) -> str:
    """Escape HTML characters"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def escape_markdown(text: str) -> str:
    """Escape Markdown characters"""
    return text.replace("_", "\\_").replace("\*", "\\*").replace("\[", "\\[").replace("\]", "\\]").replace("\(", "\\(").replace("\)", "\\)").replace("~", "\\~").replace("`", "\\`").replace("#", "\\#").replace("+", "\\+").replace("-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".", "\\.").replace("!", "\\!")

def generate_captcha() -> str:
    """Generate random captcha code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def is_admin(user_id: int, chat_id: int, app) -> bool:
    """Check if user is admin in chat"""
    try:
        member = app.get_chat_member(chat_id, user_id)
        return member.status in ["creator", "administrator"]
    except:
        return False

def is_owner(user_id: int, chat_id: int, app) -> bool:
    """Check if user is owner in chat"""
    try:
        member = app.get_chat_member(chat_id, user_id)
        return member.status == "creator"
    except:
        return False

def is_staff(user_id: int, chat_id: int, app) -> bool:
    """Check if user is staff (admin or owner)"""
    try:
        member = app.get_chat_member(chat_id, user_id)
        return member.status in ["creator", "administrator"]
    except:
        return False

def get_user_mention(user) -> str:
    """Get user mention string"""
    if user.username:
        return f"@{user.username}"
    elif user.first_name:
        if user.last_name:
            return f"{user.first_name} {user.last_name}"
        return user.first_name
    return f"User {user.id}"

def get_chat_title(chat) -> str:
    """Get chat title"""
    return chat.title or chat.first_name or "Unknown"

def parse_time(time_str: str) -> Optional[int]:
    """Parse time string to seconds"""
    time_str = time_str.lower().strip()
    
    # Parse formats: 1m, 1h, 1d, 1w
    match = re.match(r'(\d+)([smhdw])', time_str)
    if not match:
        return None
    
    value, unit = match.groups()
    value = int(value)
    
    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800,
    }
    
    return value * multipliers.get(unit, 1)

def format_time(seconds: int) -> str:
    """Format seconds to human readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    elif seconds < 86400:
        return f"{seconds // 3600}h"
    else:
        return f"{seconds // 86400}d"

def get_file_id(message) -> Optional[str]:
    """Get file_id from message"""
    if message.photo:
        return message.photo.file_id
    elif message.video:
        return message.video.file_id
    elif message.document:
        return message.document.file_id
    elif message.audio:
        return message.audio.file_id
    elif message.voice:
        return message.voice.file_id
    elif message.sticker:
        return message.sticker.file_id
    return None

def is_spam(text: str, sensitivity: int = 50) -> bool:
    """Check if text is spam (simple check)"""
    if not text:
        return False
    
    # Check for repeated characters
    if len(set(text)) < len(text) * (100 - sensitivity) / 100:
        return True
    
    # Check for all caps
    if len(text) > 10 and text.isupper():
        return True
    
    return False

def check_word_in_text(text: str, word: str) -> bool:
    """Check if word is in text (case insensitive)"""
    return word.lower() in text.lower()

def get_member_status(status: str) -> str:
    """Get human readable status"""
    statuses = {
        "creator": "Owner",
        "administrator": "Admin",
        "member": "Member",
        "restricted": "Restricted",
        "left": "Left",
        "kicked": "Kicked",
    }
    return statuses.get(status, status)

def format_user_info(user, chat_member=None) -> str:
    """Format user information"""
    info = []
    info.append(f"**ID:** `{user.id}`")
    
    if user.first_name:
        info.append(f"**Name:** {user.first_name}")
    if user.last_name:
        info.append(f"**Last Name:** {user.last_name}")
    if user.username:
        info.append(f"**Username:** @{user.username}")
    
    if chat_member:
        info.append(f"**Status:** {get_member_status(chat_member.status)}")
        if hasattr(chat_member, 'until_date') and chat_member.until_date:
            info.append(f"**Until:** {chat_member.until_date}")
    
    return "\n".join(info)

def format_chat_info(chat) -> str:
    """Format chat information"""
    info = []
    info.append(f"**ID:** `{chat.id}`")
    
    if chat.title:
        info.append(f"**Title:** {chat.title}")
    if chat.username:
        info.append(f"**Username:** @{chat.username}")
    if chat.type:
        info.append(f"**Type:** {chat.type}")
    if hasattr(chat, 'description') and chat.description:
        info.append(f"**Description:** {chat.description}")
    
    return "\n".join(info)

# ============== Language Functions ==============

LANGUAGES = {
    "he": {
        "name": "עברית",
        "code": "he",
    },
    "en": {
        "name": "English",
        "code": "en",
    },
    "ar": {
        "name": "العربية",
        "code": "ar",
    },
    "es": {
        "name": "Español",
        "code": "es",
    },
    "fr": {
        "name": "Français",
        "code": "fr",
    },
    "de": {
        "name": "Deutsch",
        "code": "de",
    },
    "ru": {
        "name": "Русский",
        "code": "ru",
    },
}

def get_language_list() -> str:
    """Get list of available languages"""
    text = "**Available Languages:**\n\n"
    for lang in LANGUAGES.values():
        text += f"• `{lang['code']}` - {lang['name']}\n"
    return text

def get_language(code: str) -> Optional[Dict]:
    """Get language by code"""
    return LANGUAGES.get(code)

# ============== Translation Functions ==============

def t(key: str, lang: str = "he") -> str:
    """Get translation for key"""
    translations = {
        "he": {
            "welcome": "ברוך הבא {first}!",
            "welcome_group": "ברוך הבא {first} לקבוצה {group}!",
            "left": "להתראות {first}! נשמח לראותך שוב.",
            "promoted": "{user} הועלה לדרגת {rank}!",
            "demoted": "{user} הוסר מדרגת {rank}!",
            "banned": "{user} נחסם מהקבוצה!",
            "unbanned": "{user} הוסר מהחסימה!",
            "kicked": "{user} הוצא מהקבוצה!",
            "muted": "{user} הושתק למשך {time}!",
            "unmuted": "{user} הוסר ההשתקה!",
            "warned": "{user} קיבל אזהרה! סיבה: {reason}\nאזהרות: {count}/{max}",
            "warns_cleared": "אזהרות של {user} נמחקו!",
            "pinned": "ההודעה ננעלה!",
            "unpinned": "ההודעה שוחררה!",
            "deleted": "ההודעות נמחקו!",
            "no_permission": "אין לך הרשאה לבצע פעולה זו!",
            "user_not_found": "משתמש לא נמצא!",
            "group_not_found": "קבוצה לא נמצאה!",
            "already_admin": "המשתמש כבר מנהל!",
            "not_admin": "המשתמש אינו מנהל!",
            "settings_saved": "ההגדרות נשמרו!",
            "lock_enabled": "{item} ננעל!",
            "lock_disabled": "{item} נפתח!",
            "filter_added": "המסנן נוסף!",
            "filter_removed": "המסנן הוסר!",
            "note_added": "ההערה נוספה!",
            "note_removed": "ההערה נמחקה!",
            "rules_set": "הכללים נקבעו!",
            "welcome_set": "הברכה נקבעה!",
            "language_set": "השפה שונתה ל{lang}!",
            "antiflood_enabled": "הגנה מפני הצפות הופעלה!",
            "antiflood_disabled": "הגנה מפני הצפות כבויה!",
            "captcha_enabled": "CAPTCHA הופעל!",
            "captcha_disabled": "CAPTCHA כבוי!",
            "id_result": "מזהה משתמש: `{user_id}`\nמזהה קבוצה: `{chat_id}`",
            "info_result": "מידע על המשתמש:\n{info}",
            "chat_info_result": "מידע על הקבוצה:\n{info}",
            "staff_list": "צוות הקבוצה:\n{staff}",
            "no_staff": "אין צוות בקבוצה זו.",
            "rules": "כללי הקבוצה:\n{rules}",
            "no_rules": "אין כללים בקבוצה זו.",
            "notes_list": "הערות בקבוצה:\n{notes}",
            "no_notes": "אין הערות בקבוצה זו.",
            "filters_list": "מסננים בקבוצה:\n{filters}",
            "no_filters": "אין מסננים בקבוצה זו.",
            "blocklist_added": "{word} נוסף לרשימת החסימה!",
            "blocklist_removed": "{word} הוסר מרשימת החסימה!",
            "blocklist_list": "רשימת החסימה:\n{words}",
            "no_blocklist": "רשימת החסימה ריקה.",
            "help": "**עזרה**\n\nפקודות זמינות:\n{commands}",
            "help_admin": "**עזרה למנהלים**\n\nפקודות:\n{commands}",
        },
        "en": {
            "welcome": "Welcome {first}!",
            "welcome_group": "Welcome {first} to {group}!",
            "left": "Goodbye {first}! See you again.",
            "promoted": "{user} promoted to {rank}!",
            "demoted": "{user} demoted from {rank}!",
            "banned": "{user} banned from the group!",
            "unbanned": "{user} unbanned!",
            "kicked": "{user} kicked from the group!",
            "muted": "{user} muted for {time}!",
            "unmuted": "{user} unmuted!",
            "warned": "{user} warned! Reason: {reason}\nWarnings: {count}/{max}",
            "warns_cleared": "{user}'s warnings cleared!",
            "pinned": "Message pinned!",
            "unpinned": "Message unpinned!",
            "deleted": "Messages deleted!",
            "no_permission": "You don't have permission!",
            "user_not_found": "User not found!",
            "group_not_found": "Group not found!",
            "already_admin": "User is already admin!",
            "not_admin": "User is not admin!",
            "settings_saved": "Settings saved!",
            "lock_enabled": "{item} locked!",
            "lock_disabled": "{item} unlocked!",
            "filter_added": "Filter added!",
            "filter_removed": "Filter removed!",
            "note_added": "Note added!",
            "note_removed": "Note removed!",
            "rules_set": "Rules set!",
            "welcome_set": "Welcome message set!",
            "language_set": "Language changed to {lang}!",
            "antiflood_enabled": "Anti-flood enabled!",
            "antiflood_disabled": "Anti-flood disabled!",
            "captcha_enabled": "CAPTCHA enabled!",
            "captcha_disabled": "CAPTCHA disabled!",
            "id_result": "User ID: `{user_id}`\nChat ID: `{chat_id}`",
            "info_result": "User info:\n{info}",
            "chat_info_result": "Group info:\n{info}",
            "staff_list": "Group staff:\n{staff}",
            "no_staff": "No staff in this group.",
            "rules": "Group rules:\n{rules}",
            "no_rules": "No rules in this group.",
            "notes_list": "Notes in group:\n{notes}",
            "no_notes": "No notes in this group.",
            "filters_list": "Filters in group:\n{filters}",
            "no_filters": "No filters in this group.",
            "blocklist_added": "{word} added to blocklist!",
            "blocklist_removed": "{word} removed from blocklist!",
            "blocklist_list": "Blocklist:\n{words}",
            "no_blocklist": "Blocklist is empty.",
            "help": "**Help**\n\nAvailable commands:\n{commands}",
            "help_admin": "**Admin Help**\n\nCommands:\n{commands}",
        },
    }
    
    return translations.get(lang, translations["he"]).get(key, key)

def tr(key: str, lang: str = "he", **kwargs) -> str:
    """Get translation with parameters"""
    text = t(key, lang)
    for key, value in kwargs.items():
        text = text.replace(f"{{{key}}}", str(value))
    return text