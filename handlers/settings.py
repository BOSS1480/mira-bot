"""
Settings and basic handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from database import ConnectedChats, get_session
from sqlalchemy import select
from utils import tr, get_lang

# Start handler
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    """Handle /start command"""
    chat_id = message.chat.id
    text = await tr(chat_id, "welcome_to_bot")
    await message.reply(text)

# Help keyboard for private chat
def get_help_keyboard():
    """Get help menu keyboard like MissRose"""
    keyboard = [
        [InlineKeyboardButton("📚 Moderation", "help:moderation")],
        [InlineKeyboardButton("👋 Welcome", "help:welcome")],
        [InlineKeyboardButton("🛡️ Protection", "help:protection")],
        [InlineKeyboardButton("📝 Notes & Rules", "help:notes")],
        [InlineKeyboardButton("⚙️ Settings", "help:settings")],
        [InlineKeyboardButton("🌐 Language", "help:language")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Help text sections
HELP_TEXTS = {
    "en": {
        "moderation": """
*📚 Moderation*

• /ban - Ban a user
• /unban - Unban a user  
• /mute - Mute a user
• /unmute - Unmute a user
• /kick - Kick a user
• /warn - Warn a user
• /warnings - Check warnings
• /clearwarnings - Clear warnings
• /purge - Delete messages
• /report - Report a user
""",
        "welcome": """
*👋 Welcome/Goodbye*

• /welcome - Toggle welcome
• /setwelcome <text> - Set welcome
• /setgoodbye <text> - Set goodbye

*Placeholders:*
{first}, {last}, {fullname}, {username}, {chatname}, {userid}
""",
        "protection": """
*🛡️ Protection*

• /antiflood [limit] - Enable antiflood
• /blocklist add <word> - Add to blocklist
• /blocklist remove <word> - Remove from blocklist
• /blocklist list - Show blocklist
""",
        "notes": """
*📝 Notes & Rules*

• /rules - Show rules
• /setrules <text> - Set rules
• /note <name> - Get a note
• /addnote <name> <content> - Add note
• /rmnote <name> - Remove note
• /listnotes - List notes
""",
        "settings": """
*⚙️ Settings*

• /connect <group_id> - Connect to group
• /setlang <code> - Change language
• /lang - Show current language
• /promote - Promote to admin
• /demote - Demote from admin
• /staff - List staff
• /id - Get ID
• /info - Get user info
""",
        "language": """
*🌐 Language*

Use /setlang to change bot language:
• /setlang en - English
• /setlang he - עברית

Current: /lang
"""
    },
    "he": {
        "moderation": """
*📚 מודרציה*

• /ban - חסום משתמש
• /unban - בטל חסימה
• /mute - נדה משתמש
• /unmute - בטל נידוי
• /kick - הוצא משתמש
• /warn - התראה למשתמש
• /warnings - צפה בהתראות
• /clearwarnings - נקה התראות
• /purge - מחק הודעות
• /report - דווח על משתמש
""",
        "welcome": """
*👋 קבלה/פרידה*


• /welcome - הפעל/כבה קבלה
• /setwelcome <טקסט> - קבע הודעת קבלה
• /setgoodbye <טקסט> - קבע הודעת פרידה

*מציינים:*
{first}, {last}, {fullname}, {username}, {chatname}, {userid}
""",
        "protection": """
*🛡️ הגנה*

• /antiflood [מגבלה] - הפעל הגנה מהצפה
• /blocklist add <מילה> - הוסף לרשימת חסימה
• /blocklist remove <מילה> - הסר מרשימת חסימה
• /blocklist list - הצג רשימת חסימה
""",
        "notes": """
*📝 הערות וכללים*


• /rules - הצג כללים
• /setrules <טקסט> - קבע כללים
• /note <שם> - קרא הערה
• /addnote <שם> <תוכן> - הוסף הערה
• /rmnote <שם> - מחק הערה
• /listnotes - רשימת הערות
""",
        "settings": """
*⚙️ הגדרות*

• /connect <group_id> - התחבר לקבוצה
• /setlang <קוד> - שנה שפה
• /lang - הצג שפה נוכחית
• /promote - העלה למנהל
• /demote - הורד ממנהל
• /staff - רשימת צוות
• /id - קבל מזהה
• /info - מידע על משתמש
""",
        "language": """
*🌐 שפה*

השתמש ב-/setlang כדי לשנות שפה:
• /setlang en - English
• /setlang he - עברית

נוכחי: /lang
"""
    }
}

# Help handler (private)
@Client.on_message(filters.command("help") & filters.private)
async def help_handler(client: Client, message: Message):
    """Show help menu with buttons"""
    chat_id = message.chat.id
    lang = await get_lang(chat_id)
    
    text = HELP_TEXTS.get(lang, HELP_TEXTS["en"]).get("moderation", HELP_TEXTS["en"]["moderation"])
    
    await message.reply(
        text,
        reply_markup=get_help_keyboard()
    )

# Help handler (group)
@Client.on_message(filters.command("help") & filters.group)
async def group_help_handler(client: Client, message: Message):
    """Show help in group"""
    chat_id = message.chat.id
    lang = await get_lang(chat_id)
    
    text = HELP_TEXTS.get(lang, HELP_TEXTS["en"]).get("moderation", HELP_TEXTS["en"]["moderation"])
    
    await message.reply(text)


# ID handler
@Client.on_message(filters.command("id"))
async def id_handler(client: Client, message: Message):
    """Get chat or user ID"""
    chat_id = message.chat.id
    
    if message.chat.type == "private":
        text = await tr(chat_id, "your_id", id=message.from_user.id)
    else:
        text = await tr(chat_id, "chat_id", id=message.chat.id)
    
    await message.reply(text)

# Info handler
@Client.on_message(filters.command("info"))
async def info_handler(client: Client, message: Message):
    """Get user info"""
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    chat_id = message.chat.id
    
    if not user:
        await message.reply(await tr(chat_id, "user_not_found"))
        return
    
    text = await tr(chat_id, "user_info",
        name=user.first_name or "Unknown",
        id=user.id,
        username=user.username or "None"
    )
    await message.reply(text)

# Settings handler
@Client.on_message(filters.command("settings") & filters.group)
async def settings_handler(client: Client, message: Message):
    """Show settings"""
    chat_id = message.chat.id
    text = await tr(chat_id, "settings_info")
    await message.reply(text)

# Connect handler
@Client.on_message(filters.command("connect") & filters.private)
async def connect_handler(client: Client, message: Message):
    """Connect private chat to group"""
    chat_id = message.chat.id
    
    if len(message.command) > 1:
        try:
            group_id = int(message.command[1])
        except:
            await message.reply(await tr(chat_id, "invalid_group_id"))
            return
        
        async for session in get_session():
            connected = ConnectedChats(
                chat_id=chat_id,
                connected_group_id=group_id
            )
            session.add(connected)
            await session.commit()
            await message.reply(await tr(chat_id, "connected", id=group_id))
            break
    else:
        await message.reply(await tr(chat_id, "connect_usage"))
