"""
Utilities - Translation system
"""
from database import ChatSettings, get_session
from sqlalchemy import select

# Translations
TRANSLATIONS = {
    "en": {
        # General
        "only_admins": "🚫 Only admins can use this command!",
        "invalid_user": "Invalid user ID",
        "reply_or_id": "Reply to a user or provide user ID",
        "done": "✅ Done!",
        "error": "❌ Error: {}",
        
        # Moderation
        "banned": "🚫 Banned {}",
        "unbanned": "✅ User unbanned!",
        "muted": "🔇 Muted {} for {} minutes!",
        "unmuted": "✅ User unmuted!",
        "kicked": "👢 Kicked {}!",
        "cannot_ban_admin": "Cannot ban an admin!",
        "warned": "⚠️ {} warned! ({}/{})\nReason: {}",
        "max_warnings": "⚠️ {} reached {} warnings and was banned!",
        "no_warnings": "✅ {} has no warnings!",
        "warnings_list": "⚠️ *Warnings for {}:*\n\n{}\n\nTotal: {}/{}",
        "clearwarnings_done": "✅ Cleared all warnings for {}!",
        "purge_done": "🗑️ Deleted {} messages!",
        "purge_reply": "Reply to a message to delete from",
        "reported": "✅ User reported to admins!",
        "report_reply": "Reply to a message to report",
        
        # Welcome
        "welcome_enabled": "✅ Welcome message enabled!",
        "welcome_disabled": "✅ Welcome message disabled!",
        "welcome_set": "✅ Welcome message set!\n\n{}",
        "goodbye_set": "✅ Goodbye message set!\n\n{}",
        
        # Antiflood
        "antiflood_enabled": "✅ AntiFlood enabled!\nLimit: {} messages per {} seconds",
        "antiflood_disabled": "✅ AntiFlood disabled!",
        "flood_muted": "🚫 {} muted for flooding!",
        
        # Filters
        "filter_added": "✅ Filter added!\nKeyword: {}\nResponse: {}",
        "filter_removed": "✅ Filter '{}' removed!",
        "no_filters": "No filters set!",
        "filters_list": "📋 *Filters:*\n\n{}",
        "blocklist_added": "✅ Added '{}' to blocklist!",
        "blocklist_removed": "✅ Removed '{}' from blocklist!",
        "blocklist_empty": "Blocklist is empty!",
        "blocklist_list": "🚫 *Blocklist:*\n\n{}",
        
        # Rules
        "no_rules": "No rules set yet!",
        "rules_set": "✅ Rules updated!",
        "rules_text": "📜 *Rules:*\n\n{}",
        
        # Notes
        "note_not_found": "Note '{}' not found!",
        "note_saved": "✅ Note '{}' saved!",
        "note_removed": "✅ Note '{}' removed!",
        "no_notes": "No notes saved!",
        "notes_list": "📝 *Notes:*\n\n{}",
        
        # Staff
        "promoted": "✅ {} promoted to admin!",
        "demoted": "✅ {} demoted from admin!",
        "only_creator": "🚫 Only the group creator can do this!",
        "staff_list": "👥 *Staff:*\n\n{}",
        
        # Settings
        "welcome_to_bot": "👋 Welcome to Mira Bot!\n\nI'm a powerful group management bot.\n\nAdd me to your group and make me admin to get started!\n\nUse /help to see all commands.",
        "connected": "✅ Connected to group {}!",
        "invalid_group_id": "Invalid group ID",
        "connect_usage": "Usage: /connect <group_id>",
        "settings_info": "⚙️ Use /connect to connect your private chat with this group.",
        
        # ID/Info
        "your_id": "Your ID: `{}`",
        "chat_id": "Chat ID: `{}`",
        "user_info": "👤 *User Info:*\n\n• Name: {}\n• ID: `{}`\n• Username: @{}",
        "user_not_found": "User not found!",
        
        # Language
        "lang_set": "✅ Language set to {}!",
        "lang_current": "🌐 Current language: {}",
        "lang_not_supported": "Language '{}' not supported!\nUse /setlang to see available languages.",
        "lang_list": "🌐 *Available Languages:*\n\n{}",
        "lang_usage": "Usage: /setlang <code>",
    },
    "he": {
        # General
        "only_admins": "🚫 רק מנהלים יכולים להשתמש בפקודה הזו!",
        "invalid_user": "מזהה משתמש לא תקין",
        "reply_or_id": "השב למשתמש או תן מזהה משתמש",
        "done": "✅ בוצע!",
        "error": "❌ שגיאה: {}",
        
        # Moderation
        "banned": "🚫 {} נחסם",
        "unbanned": "✅ המשתמש בוטל!",
        "muted": "🔇 {} נודה ל{} דקות!",
        "unmuted": "✅ המשתמש בוטל!",
        "kicked": "👢 {} נוצא!",
        "cannot_ban_admin": "לא ניתן לחסום מנהל!",
        "warned": "⚠️ {} התראה! ({}/{})\nסיבה: {}",
        "max_warnings": "⚠️ {} הגיע ל{} התראות ונחסם!",
        "no_warnings": "✅ ל{} אין התראות!",
        "warnings_list": "⚠️ *התראות ל{}:*\n\n{}\n\nסה"כ: {}/{}",
        "clearwarnings_done": "✅ כל ההתראות של {} נמחקו!",
        "purge_done": "🗑️ נמחקו {} הודעות!",
        "purge_reply": "השב להודעה כדי למחוק ממנה",
        "reported": "✅ המשתמש דווח למנהלים!",
        "report_reply": "השב להודעה כדי לדווח",
        
        # Welcome
        "welcome_enabled": "✅ הודעת קבלה הופעלה!",
        "welcome_disabled": "✅ הודעת קבלה כובתה!",
        "welcome_set": "✅ הודעת קבלה נקבעה!\n\n{}",
        "goodbye_set": "✅ הודעת פרידה נקבעה!\n\n{}",
        
        # Antiflood
        "antiflood_enabled": "✅ AntiFlood הופעל!\nמגבלה: {} הודעות ב{} שניות",
        "antiflood_disabled": "✅ AntiFlood כובה!",
        "flood_muted": "🚫 {} נודה בגלל הצפה!",
        
        # Filters
        "filter_added": "✅ מסנן נוסף!\nמילת מפתח: {}\nתגובה: {}",
        "filter_removed": "✅ המסנן '{}' הוסר!",
        "no_filters": "אין מסננים!",
        "filters_list": "📋 *מסננים:*\n\n{}",
        "blocklist_added": "✅ '{}' נוסף לרשימת החסימה!",
        "blocklist_removed": "✅ '{}' הוסר מרשימת החסימה!",
        "blocklist_empty": "רשימת החסימה ריקה!",
        "blocklist_list": "🚫 *רשימת חסימה:*\n\n{}",
        
        # Rules
        "no_rules": "אין כללים עדיין!",
        "rules_set": "✅ הכללים עודכנו!",
        "rules_text": "📜 *כללים:*\n\n{}",
        
        # Notes
        "note_not_found": "ההערה '{}' לא נמצאה!",
        "note_saved": "✅ ההערה '{}' נשמרה!",
        "note_removed": "✅ ההערה '{}' נמחקה!",
        "no_notes": "אין הערות שמורות!",
        "notes_list": "📝 *הערות:*\n\n{}",
        
        # Staff
        "promoted": "✅ {} הועלה למנהל!",
        "demoted": "✅ {} הורד ממנהל!",
        "only_creator": "רק יוצר הקבוצה יכול לעשות את זה!",
        "staff_list": "👥 *צוות:*\n\n{}",
        
        # Settings
        "welcome_to_bot": "👋 ברוך הבא ל-Mira Bot!\n\nאני בוט ניהול קבוצות חזק.\n\nהוסף אותי לקבוצה שלך ותן לי הרשאות מנהל כדי להתחיל!\n\nהשתמש ב-/help כדי לראות את כל הפקודות.",
        "connected": "✅ התחברת לקבוצה {}!",
        "invalid_group_id": "מזהה קבוצה לא תקין",
        "connect_usage": "שימוש: /connect <group_id>",
        "settings_info": "⚙️ השתמש ב-/connect כדי לחבר את הצ'אט הפרטי שלך עם הקבוצה הזו.",
        
        # ID/Info
        "your_id": "המזהה שלך: `{}`",
        "chat_id": "מזהה הצ'אט: `{}`",
        "user_info": "👤 *מידע על המשתמש:*\n\n• שם: {}\n• מזהה: `{}`\n• שם משתמש: @{}",
        "user_not_found": "משתמש לא נמצא!",
        
        # Language
        "lang_set": "✅ השפה הוגדרה ל{}!",
        "lang_current": "🌐 השפה הנוכחית: {}",
        "lang_not_supported": "השפה '{}' לא נתמכת!\nהשתמש ב-/setlang כדי לראות את השפות הזמינות.",
        "lang_list": "🌐 *שפות זמינות:*\n\n{}",
        "lang_usage": "שימוש: /setlang <קוד>",
    }
}

async def get_lang(chat_id: int) -> str:
    """Get chat language"""
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        return settings.lang if settings else "en"

def t(chat_id: int, key: str, **kwargs) -> str:
    """Translate a key"""
    # Default to English
    lang = "en"
    
    if key not in TRANSLATIONS[lang]:
        return key
    
    text = TRANSLATIONS[lang].get(key, key)
    
    # Replace placeholders
    for k, v in kwargs.items():
        text = text.replace("{" + k + "}", str(v))
    
    return text

async def tr(chat_id: int, key: str, **kwargs) -> str:
    """Async translate with chat language"""
    lang = await get_lang(chat_id)
    if lang not in TRANSLATIONS:
        lang = "en"
    
    if key not in TRANSLATIONS.get(lang, TRANSLATIONS["en"]):
        return key
    
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    
    for k, v in kwargs.items():
        text = text.replace("{" + k + "}", str(v))
    
    return text

# Helper for markdown escape
def escape_md(text: str) -> str:
    """Escape markdown special characters"""
    special = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special:
        text = text.replace(char, f"\\{char}")
    return text