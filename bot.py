\"""
Mira Bot - Telegram Group Management Bot
Main entry point - MissRose inspired
"""
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message


from config import BOT_TOKEN
from database import init_db
from handlers import (
    moderation, welcome, antiflood, filters as filter_handler,
    rules, notes, staff, settings, language
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create bot client
app = Client(
    "mira_bot",
    bot_token=BOT_TOKEN,
    workdir="."
)

# Register handlers
def register_handlers():
    """Register all message handlers"""
    
    # Basic handlers
    app.add_handler(filters.command("start") & filters.private, settings.start_handler)
    app.add_handler(filters.command("help"), settings.help_handler)
    app.add_handler(filters.command("id"), settings.id_handler)
    app.add_handler(filters.command("info"), settings.info_handler)
    
    # Moderation handlers
    app.add_handler(moderation.ban_handler)
    app.add_handler(moderation.unban_handler)
    app.add_handler(moderation.mute_handler)
    app.add_handler(moderation.unmute_handler)
    app.add_handler(moderation.kick_handler)
    app.add_handler(moderation.warn_handler)
    app.add_handler(moderation.warnings_handler)
    app.add_handler(moderation.clearwarnings_handler)
    app.add_handler(moderation.purge_handler)
    app.add_handler(moderation.report_handler)
    
    # Welcome/Goodbye handlers
    app.add_handler(welcome.welcome_handler)
    app.add_handler(welcome.goodbye_handler)
    app.add_handler(welcome.set_welcome_handler)
    app.add_handler(welcome.set_goodbye_handler)
    app.add_handler(welcome.welcome_toggle_handler)
    
    # Antiflood handler
    app.add_handler(antiflood.flood_handler)
    app.add_handler(antiflood.antiflood_handler)
    
    # Filters handler
    app.add_handler(filter_handler.filter_handler)
    app.add_handler(filter_handler.add_filter_handler)
    app.add_handler(filter_handler.rm_filter_handler)
    app.add_handler(filter_handler.list_filters_handler)
    app.add_handler(filter_handler.blocklist_handler)
    
    # Rules handlers
    app.add_handler(rules.rules_handler)
    app.add_handler(rules.set_rules_handler)
    
    # Notes handlers
    app.add_handler(notes.note_handler)
    app.add_handler(notes.add_note_handler)
    app.add_handler(notes.rm_note_handler)
    app.add_handler(notes.list_notes_handler)
    
    # Staff handlers
    app.add_handler(staff.promote_handler)
    app.add_handler(staff.demote_handler)
    app.add_handler(staff.staff_handler)
    
    # Settings handlers
    app.add_handler(settings.settings_handler)
    app.add_handler(settings.connect_handler)
    
    # Language handlers
    app.add_handler(language.setlang_handler)
    app.add_handler(language.lang_handler)

async def main():
    """Main function to start the bot"""
    logger.info("Starting Mira Bot...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Register handlers
    register_handlers()
    logger.info("Handlers registered")
    
    # Start bot
    await app.start()
    me = await app.get_me()
    logger.info(f"Mira Bot started as @{me.username}")
    
    # Run until disconnected
    await app.idle()
    
    await app.stop()
    logger.info("Mira Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())