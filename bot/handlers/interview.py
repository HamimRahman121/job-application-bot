"""
/interview command — Interview preparation guide
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import get_interview_questions
from bot.services.database import save_analysis
from bot.utils.helpers import split_message, get_thinking_message


PROMPT_TEXT = """
🎤 *Interview Prep Guide*

What job role are you interviewing for?

Just type the job title, for example:
• `Python Developer`
• `Data Scientist`
• `Product Manager`
• `UX Designer`
• `DevOps Engineer`

I'll give you real interview questions, sample answers, and insider tips! 🚀
"""


async def interview_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /interview command."""
    context.user_data["mode"] = "interview"
    await update.message.reply_text(PROMPT_TEXT, parse_mode="Markdown")


async def handle_interview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate interview prep guide for the given role."""
    user = update.effective_user
    job_role = update.message.text.strip()

    if len(job_role) < 3:
        await update.message.reply_text("⚠️ Please enter a valid job title (e.g. 'Software Engineer').")
        return

    if len(job_role) > 100:
        await update.message.reply_text("⚠️ Job title seems too long. Please just type the role name.")
        return

    thinking_msg = await update.message.reply_text(get_thinking_message("interview"))

    result = get_interview_questions(job_role)

    await thinking_msg.delete()

    save_analysis(
        user_id=user.id,
        username=user.username or user.first_name,
        action="interview",
        input_text=job_role,
        result_text=result,
    )

    header = f"🎤 *Interview Guide: {job_role}*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    chunks = split_message(header + result)
    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode="Markdown")

    context.user_data.pop("mode", None)
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *Interview guide ready!* Study these questions carefully.\n\n"
        "🍀 *Good luck with your interview!*\n\n"
        "💡 Also try:\n"
        "• /tips — General job hunting strategies\n"
        "• /linkedin — Optimise your LinkedIn before the interview",
        parse_mode="Markdown",
    )
