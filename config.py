import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_ID = ""
BOT_NAME = "Mira Bot"
BOT_USERNAME = ""

# Database
DB_URI = "sqlite:///mira.db"

# Channels
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "")

# Settings
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "")

# Languages
DEFAULT_LANGUAGE = "he"

# Flood
FLOOD_LIMIT = 5
FLOOD_TIME = 6

# Warnings
MAX_WARNINGS = 3

# Anti-Spam
ANTISPAM_SENSITIVITY = 50

# Welcome
WELCOME_ENABLED = True
WELCOME_MESSAGES = [
    "Welcome {first}!",
    "Hello {first}! Welcome to {group}",
]

# Admin
ADMINS = []  # Add admin user IDs here

# Group Settings
GROUP_LOCKS = {
    "stickers": False,
    "photos": False,
    "videos": False,
    "documents": False,
    "games": False,
    "inline": False,
    "polls": False,
    "voice": False,
    "videochat": False,
    "location": False,
    "contacts": False,
    "rtl": False,
    "button": False,
    "eggs": False,
}

# Blocklist
BLOCK_WORD = []
SPAM_WORDS = []

# Notes
NOTES = {}

# Filters
FILTERS = {}

# Chatbot
CHATBOT_ENABLED = False
CHATBOT_MODE = "false"

# AI
AI_ENABLED = False
AI_API_KEY = ""

# Captcha
CAPTCHA_ENABLED = False
CAPTCHA_TIME = 60

# Rules
RULES_DEFAULT = "No rules yet."

# Staff
STAFF_ROLES = {
    "owner": 5,
    "admin": 4,
    "moderator": 3,
    "vip": 2,
    "member": 1,
}