"""
/analyze command — CV analysis handler
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import analyze_cv
from bot.services.database import save_analysis
from bot.utils.helpers import split_message, get_thinking_message


PROMPT_TEXT = """
📄 *CV Analyser*

Please paste your full CV text below.

Just copy all the text from your CV and send it here — I'll give you expert feedback! ✨

💡 *Tip:* The more complete your CV text, the better the analysis.
"""


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /analyze command — ask user for their CV."""
    context.user_data["mode"] = "analyze"
    await update.message.reply_text(PROMPT_TEXT, parse_mode="Markdown")


async def handle_analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the CV text and return AI analysis."""
    user = update.effective_user
    cv_text = update.message.text.strip()

    if len(cv_text) < 50:
        await update.message.reply_text(
            "⚠️ That seems too short to be a CV!\n\n"
            "Please paste the full text of your CV (copy everything from your CV document)."
        )
        return

    thinking_msg = await update.message.reply_text(get_thinking_message("analyze"))
    result = await analyze_cv(cv_text)
    await thinking_msg.delete()

    save_analysis(
        user_id=user.id,
        username=user.username or user.first_name,
        action="analyze",
        input_text=cv_text,
        result_text=result,
    )

    chunks = split_message("📄 *CV Analysis Results*\n━━━━━━━━━━━━━━━━━━━━━\n\n" + result)
    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode="Markdown")

    context.user_data.pop("mode", None)
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *Analysis complete!*\n\n"
        "What would you like to do next?\n"
        "• /match — See how your CV matches a job\n"
        "• /coverletter — Generate a cover letter\n"
        "• /interview — Prepare for interviews",
        parse_mode="Markdown",
    )
