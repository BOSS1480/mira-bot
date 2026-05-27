\"""
Language handlers
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from database import ChatSettings, get_session
from sqlalchemy import select

# Languages supported
LANGUAGES = {
    "en": "English",
    "he": "Hebrew",
    "ar": "Arabic",
    "es": "Spanish",
    "ru": "Russian",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "tr": "Turkish",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "hi": "Hindi",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ms": "Malay",
    "fa": "Persian",
    "ur": "Urdu",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "gu": "Gujarati",
    "mr": "Marathi",
    "pa": "Punjabi",
    "uk": "Ukrainian",
    "pl": "Polish",
    "nl": "Dutch",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
}

# Setlang command
@Client.on_message(filters.command("setlang") & filters.group)
async def setlang_handler(client: Client, message: Message):
    """Set bot language"""
    if not message.from_user:
        return
    
    from handlers.moderation import is_admin
    
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        await message.reply("🚫 Only admins can use this command!")
        return
    
    if len(message.command) > 1:
        lang = message.command[1].lower()
    else:
        text = "🌐 *Available Languages:*\n\n"
        for code, name in LANGUAGES.items():
            text += f"• {code} - {name}\n"
        text += "\nUsage: /setlang <code>"
        await message.reply(text)
        return
    
    if lang not in LANGUAGES:
        await message.reply(f"Language '{lang}' not supported!\nUse /setlang to see available languages.")
        return
    
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            settings = ChatSettings(chat_id=chat_id, lang=lang)
            session.add(settings)
        else:
            settings.lang = lang
        
        await session.commit()
        await message.reply(f"✅ Language set to {LANGUAGES[lang]}!")
        break

# Lang command (show current language)
@Client.on_message(filters.command("lang") & filters.group)
async def lang_handler(client: Client, message: Message):
    """Show current language"""
    chat_id = message.chat.id
    
    async for session in get_session():
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        settings = result.scalar_one_or_none()
        
        lang = settings.lang if settings else "en"
        await message.reply(f"🌐 Current language: {LANGUAGES.get(lang, 'English')}")
        break