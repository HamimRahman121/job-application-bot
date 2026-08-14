"""
main.py — Entry point for the Job Application Helper Bot
Run with:  python main.py
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


# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""

    # Validate config
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN is missing! Please set it in your .env file.")
        raise SystemExit(1)

    # Initialise database
    init_db()
    logger.info("✅ Database initialised")

    # Build the application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # ── Register command handlers ──────────────────────────────────────────────
    app.add_handler(CommandHandler("start",       start_command))
    app.add_handler(CommandHandler("help",        help_command))
    app.add_handler(CommandHandler("analyze",     analyze_command))
    app.add_handler(CommandHandler("match",       match_command))
    app.add_handler(CommandHandler("coverletter", coverletter_command))
    app.add_handler(CommandHandler("interview",   interview_command))
    app.add_handler(CommandHandler("tips",        tips_command))
    app.add_handler(CommandHandler("linkedin",    linkedin_command))
    app.add_handler(CommandHandler("history",     history_command))

    # ── Inline keyboard button handler ────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(button_callback))

    # ── Plain text message router ─────────────────────────────────────────────
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ── Start polling ──────────────────────────────────────────────────────────
    logger.info(f"🤖 Job Application Helper Bot v{BOT_VERSION} is starting...")
    logger.info("📡 Polling for messages... Press Ctrl+C to stop.")

    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
