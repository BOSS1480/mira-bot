\"""
Mira Bot Configuration
"""
import os

# Bot Settings
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
BOT_NAME = "Mira Bot"
BOT_USERNAME = "mira_bot"

# Database
DATABASE_URL = "sqlite+aiosqlite:///bot.db"

# Default Settings
DEFAULT_WELCOME = "Welcome {first} to {chatname}!"
DEFAULT_GOODBYE = "Goodbye {first}!"
MAX_WARNINGS = 3

# Antiflood Settings
ANTIFLOOD_LIMIT = 5
ANTIFLOOD_TIME = 5  # seconds

# AntiRaid Settings
RAID_TIME = 10  # seconds
RAID_COUNT = 10  # users joining in that time

# CAPTCHA Settings
CAPTCHA_TIME = 120  # seconds to solve CAPTCHA

# Supported Languages
LANGUAGES = {
    "en": "English",
    "he": "Hebrew",
    "ar": "Arabic",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ru": "Russian",
    "it": "Italian",
    "pt": "Portuguese",
    "tr": "Turkish",
    "id": "Indonesian",
    "hi": "Hindi",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
}