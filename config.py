# Configuration
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Default settings
DEFAULT_WELCOME = "Welcome {first} to {chatname}!"
DEFAULT_GOODBYE = "Goodbye {first}!"
MAX_WARNINGS = 3
ANTIFLOOD_LIMIT = 5
ANTIFLOOD_TIME = 5  # seconds