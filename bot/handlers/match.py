"""
/match command — CV vs Job Description matcher
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import match_cv_to_job
from bot.services.database import save_analysis
from bot.utils.helpers import split_message, get_thinking_message


PROMPT_TEXT = """
🎯 *Job Description Matcher*

Send me your CV and the Job Description in this format:

```
CV:
[Paste your full CV text here]

JOB:
[Paste the full job description here]
```

I'll calculate your match score and tell you exactly how to improve! 🚀
"""


async def match_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /match command."""
    context.user_data["mode"] = "match"
    await update.message.reply_text(PROMPT_TEXT, parse_mode="Markdown")


async def handle_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process CV + Job Description and return match analysis."""
    user = update.effective_user
    text = update.message.text.strip()

    # Parse CV and JOB sections
    text_upper = text.upper()
    if "CV:" not in text_upper or "JOB:" not in text_upper:
        await update.message.reply_text(
            "⚠️ *Format not recognised!*\n\n"
            "Please use this exact format:\n\n"
            "```\nCV:\n[Your CV text here]\n\nJOB:\n[Job description here]\n```",
            parse_mode="Markdown",
        )
        return

    # Split on CV: and JOB: (case-insensitive)
    import re
    parts = re.split(r"(?i)\bCV:\s*", text, maxsplit=1)
    if len(parts) < 2:
        await update.message.reply_text("⚠️ Could not find the CV section. Please check your format.")
        return

    remainder = parts[1]
    job_parts = re.split(r"(?i)\bJOB:\s*", remainder, maxsplit=1)
    if len(job_parts) < 2:
        await update.message.reply_text("⚠️ Could not find the JOB section. Please check your format.")
        return

    cv_text = job_parts[0].strip()
    job_text = job_parts[1].strip()

    if len(cv_text) < 30 or len(job_text) < 30:
        await update.message.reply_text("⚠️ Both your CV and the Job Description seem too short. Please add more detail.")
        return

    # Show thinking message
    thinking_msg = await update.message.reply_text(get_thinking_message("match"))

    # Get AI result
    result = match_cv_to_job(cv_text, job_text)

    await thinking_msg.delete()

    # Save to DB
    save_analysis(
        user_id=user.id,
        username=user.username or user.first_name,
        action="match",
        input_text=f"CV: {cv_text[:200]}... JOB: {job_text[:200]}...",
        result_text=result,
    )

    # Send result
    header = "🎯 *Job Match Analysis*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    chunks = split_message(header + result)
    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode="Markdown")

    context.user_data.pop("mode", None)
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *Match analysis complete!*\n\n"
        "Ready to apply? Try:\n"
        "• /coverletter — Generate a tailored cover letter\n"
        "• /interview — Prepare for the interview",
        parse_mode="Markdown",
    )
