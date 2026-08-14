"""
/linkedin command — LinkedIn profile optimiser
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import improve_linkedin
from bot.services.database import save_analysis
from bot.utils.helpers import split_message, get_thinking_message


PROMPT_TEXT = """
🔗 *LinkedIn Profile Optimiser*

Paste any section of your LinkedIn profile and I'll rewrite it to:

✅ Rank higher in recruiter searches
✅ Use the right industry keywords
✅ Sound more professional and compelling
✅ Get you more profile views & connections

*Good sections to optimise:*
• Your About/Summary section
• A specific job Experience entry
• Your Skills section
• Your Headline

Just paste the text below! 👇
"""


async def linkedin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /linkedin command."""
    context.user_data["mode"] = "linkedin"
    await update.message.reply_text(PROMPT_TEXT, parse_mode="Markdown")


async def handle_linkedin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Optimise the LinkedIn profile section."""
    user = update.effective_user
    profile_text = update.message.text.strip()

    if len(profile_text) < 20:
        await update.message.reply_text(
            "⚠️ That seems too short! Please paste a proper LinkedIn section "
            "(your About, a job description, etc.)."
        )
        return

    thinking_msg = await update.message.reply_text(get_thinking_message("linkedin"))
    result = await improve_linkedin(profile_text)
    await thinking_msg.delete()

    save_analysis(
        user_id=user.id,
        username=user.username or user.first_name,
        action="linkedin",
        input_text=profile_text,
        result_text=result,
    )

    chunks = split_message("🔗 *LinkedIn Optimisation Results*\n━━━━━━━━━━━━━━━━━━━━━\n\n" + result)
    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode="Markdown")

    context.user_data.pop("mode", None)
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *LinkedIn section optimised!*\n\n"
        "Copy the improved text above and update your LinkedIn profile.\n\n"
        "💡 *Also try:*\n"
        "• /analyze — Get your full CV reviewed\n"
        "• /tips — LinkedIn networking strategies",
        parse_mode="Markdown",
    )
