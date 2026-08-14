"""
/start and /help command handlers
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


START_TEXT = """
👋 *Welcome to Job Application Helper Bot!*

I'm your personal AI-powered career assistant. I'll help you:

📄 *Analyse* your CV and get expert feedback
🎯 *Match* your CV to any job description
✍️ *Generate* professional cover letters
🎤 *Prepare* for interviews with role-specific Q&A
🔗 *Optimise* your LinkedIn profile
💡 *Get* the best job hunting strategies

━━━━━━━━━━━━━━━━━━━━━
*🚀 Quick Start — Choose a feature below!*
━━━━━━━━━━━━━━━━━━━━━
"""

HELP_TEXT = """
📚 *All Available Commands*

━━━━━━━━━━━━━━━━━━━━━
📄 `/analyze` — Analyse your CV
🎯 `/match` — Match CV to a Job Description
✍️ `/coverletter` — Generate a Cover Letter
🎤 `/interview` — Interview Prep Guide
🔗 `/linkedin` — Optimise LinkedIn Profile
💡 `/tips` — Job Hunting Tips & Strategies
📜 `/history` — View your past analyses
ℹ️ `/help` — Show this help message
━━━━━━━━━━━━━━━━━━━━━

💡 *How to use each command:*

Simply type the command and follow the bot's instructions. I'll ask you for the information I need step by step.

*Example:*
1. Type `/analyze`
2. I ask: "Please paste your CV text"
3. You paste your CV
4. I give you a full professional analysis! ✨

━━━━━━━━━━━━━━━━━━━━━
Built with ❤️ using Python + LLaMA 3.3
"""


def get_main_keyboard():
    """Returns the main feature keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("📄 Analyse CV",        callback_data="cmd_analyze"),
            InlineKeyboardButton("🎯 Job Match",         callback_data="cmd_match"),
        ],
        [
            InlineKeyboardButton("✍️ Cover Letter",      callback_data="cmd_coverletter"),
            InlineKeyboardButton("🎤 Interview Prep",    callback_data="cmd_interview"),
        ],
        [
            InlineKeyboardButton("🔗 LinkedIn Optimiser", callback_data="cmd_linkedin"),
            InlineKeyboardButton("💡 Job Tips",          callback_data="cmd_tips"),
        ],
        [
            InlineKeyboardButton("📜 My History",        callback_data="cmd_history"),
            InlineKeyboardButton("❓ Help",               callback_data="cmd_help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        START_TEXT,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button presses."""
    query = update.callback_query
    await query.answer()

    command_map = {
        "cmd_analyze":     "📄 *CV Analyser*\n\nPlease send me your CV text.\n\nJust copy and paste the full text of your CV into the chat, then I'll give you a detailed professional analysis! ✨",
        "cmd_match":       "🎯 *Job Description Matcher*\n\nPlease send me your details in this format:\n\n```\nCV:\n[Paste your CV here]\n\nJOB:\n[Paste the job description here]\n```\n\nI'll calculate your match score and tell you exactly what to improve!",
        "cmd_coverletter": "✍️ *Cover Letter Generator*\n\nPlease send me your details in this format:\n\n```\nNAME: John Smith\nJOB: Software Engineer\nCOMPANY: Google\nSKILLS: Python, 3 years exp, Django, REST APIs\n```\n\nI'll write you a professional cover letter! 📝",
        "cmd_interview":   "🎤 *Interview Prep*\n\nWhat job role are you interviewing for?\n\nJust type the job title, e.g:\n• `Software Engineer`\n• `Data Scientist`\n• `Product Manager`",
        "cmd_linkedin":    "🔗 *LinkedIn Optimiser*\n\nPaste your LinkedIn *About* section or *Experience* text and I'll rewrite and optimise it for maximum recruiter visibility! 🚀",
        "cmd_tips":        "💡 *Job Hunting Tips*\n\nWhat topic do you want tips on? Just type it!\n\nExamples:\n• `getting my first tech job`\n• `salary negotiation`\n• `remote work`\n• `career change`\n• `networking on LinkedIn`",
        "cmd_history":     None,
        "cmd_help":        None,
    }

    if query.data == "cmd_history":
        from bot.handlers.history import show_history_inline
        await show_history_inline(update, context)
        return

    if query.data == "cmd_help":
        await query.message.reply_text(HELP_TEXT, parse_mode="Markdown", reply_markup=get_main_keyboard())
        return

    prompt = command_map.get(query.data)
    if prompt:
        context.user_data["mode"] = query.data.replace("cmd_", "")
        await query.message.reply_text(prompt, parse_mode="Markdown")
