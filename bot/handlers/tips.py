"""
/tips command — Job hunting tips
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import get_job_tips
from bot.services.database import save_analysis
from bot.utils.helpers import split_message, get_thinking_message


PROMPT_TEXT = """
💡 *Job Hunting Tips*

What topic do you want tips on?

Type your topic or question, for example:
• `getting my first tech job`
• `salary negotiation`
• `switching careers to AI`
• `how to network on LinkedIn`
• `remote work opportunities`
• `how to write a great CV`

Or just type `general` for all-round job hunting advice!
"""


async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tips command."""
    context.user_data["mode"] = "tips"
    await update.message.reply_text(PROMPT_TEXT, parse_mode="Markdown")


async def handle_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate job hunting tips for the given topic."""
    user = update.effective_user
    topic = update.message.text.strip()

    if len(topic) < 2:
        topic = "general job hunting"

    thinking_msg = await update.message.reply_text(get_thinking_message("tips"))

    result = get_job_tips(topic)

    await thinking_msg.delete()

    save_analysis(
        user_id=user.id,
        username=user.username or user.first_name,
        action="tips",
        input_text=topic,
        result_text=result,
    )

    header = f"💡 *Job Tips: {topic.title()}*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    chunks = split_message(header + result)
    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode="Markdown")

    context.user_data.pop("mode", None)
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *Tips delivered!*\n\n"
        "What else can I help you with?\n"
        "• /analyze — Review your CV\n"
        "• /match — Match CV to a job\n"
        "• /coverletter — Write a cover letter",
        parse_mode="Markdown",
    )
