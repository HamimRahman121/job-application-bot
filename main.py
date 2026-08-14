"""
main.py — Entry point for the Job Application Helper Bot
"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN, BOT_VERSION
from bot.services.database import init_db
from bot.handlers.start          import start_command, help_command, button_callback
from bot.handlers.analyze        import analyze_command
from bot.handlers.match          import match_command
from bot.handlers.coverletter    import coverletter_command
from bot.handlers.interview      import interview_command
from bot.handlers.tips           import tips_command
from bot.handlers.linkedin       import linkedin_command
from bot.handlers.history        import history_command
from bot.handlers.message_router import handle_message


logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN is missing!")
        raise SystemExit(1)

    init_db()
    logger.info("✅ Database initialised")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",       start_command))
    app.add_handler(CommandHandler("help",        help_command))
    app.add_handler(CommandHandler("analyze",     analyze_command))
    app.add_handler(CommandHandler("match",       match_command))
    app.add_handler(CommandHandler("coverletter", coverletter_command))
    app.add_handler(CommandHandler("interview",   interview_command))
    app.add_handler(CommandHandler("tips",        tips_command))
    app.add_handler(CommandHandler("linkedin",    linkedin_command))
    app.add_handler(CommandHandler("history",     history_command))

    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info(f"🤖 Job Application Helper Bot v{BOT_VERSION} is starting...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
