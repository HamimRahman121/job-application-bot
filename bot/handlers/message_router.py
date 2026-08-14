"""
Message Router — Handles all plain-text messages.
Routes each message to the correct handler based on the user's current mode.
"""

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.analyze     import handle_analyze
from bot.handlers.match       import handle_match
from bot.handlers.coverletter import handle_coverletter
from bot.handlers.interview   import handle_interview
from bot.handlers.tips        import handle_tips
from bot.handlers.linkedin    import handle_linkedin


ROUTER = {
    "analyze":     handle_analyze,
    "match":       handle_match,
    "coverletter": handle_coverletter,
    "interview":   handle_interview,
    "tips":        handle_tips,
    "linkedin":    handle_linkedin,
}

NO_MODE_TEXT = """
👋 *Hey there!*

Not sure what to do? Use one of these commands:

📄 /analyze — Analyse your CV
🎯 /match — Match CV to a job description
✍️ /coverletter — Generate a cover letter
🎤 /interview — Get interview questions
🔗 /linkedin — Optimise your LinkedIn
💡 /tips — Job hunting strategies
📜 /history — View your past analyses
❓ /help — Full help menu

Or type /start to see the main menu with buttons! 🚀
"""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route incoming text messages to the correct handler."""
    mode = context.user_data.get("mode")

    if mode and mode in ROUTER:
        await ROUTER[mode](update, context)
    else:
        await update.message.reply_text(NO_MODE_TEXT, parse_mode="Markdown")
