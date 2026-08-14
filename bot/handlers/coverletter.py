"""
/coverletter command — Cover letter generator
"""

import re
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import generate_cover_letter
from bot.services.database import save_analysis
from bot.utils.helpers import split_message, get_thinking_message


PROMPT_TEXT = """
✍️ *Cover Letter Generator*

Please send your details in this format:

```
NAME: Your Full Name
JOB: Job Title You're Applying For
COMPANY: Company Name
SKILLS: Your key skills, years of experience, relevant achievements
```

*Example:*
```
NAME: Hamim Ahmed
JOB: Python Backend Developer
COMPANY: TechCorp Ltd
SKILLS: Python 3 years, Django, REST APIs, PostgreSQL, Docker, built 3 production apps
```

I'll write you a professional, tailored cover letter! 📝
"""


async def coverletter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /coverletter command."""
    context.user_data["mode"] = "coverletter"
    await update.message.reply_text(PROMPT_TEXT, parse_mode="Markdown")


async def handle_coverletter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parse user details and generate a cover letter."""
    user = update.effective_user
    text = update.message.text.strip()

    def extract_field(label: str) -> str:
        match = re.search(rf"(?i){label}:\s*(.+?)(?=\n[A-Z]+:|$)", text, re.DOTALL)
        return match.group(1).strip() if match else ""

    name    = extract_field("NAME")
    job     = extract_field("JOB")
    company = extract_field("COMPANY")
    skills  = extract_field("SKILLS")

    if not all([name, job, company, skills]):
        await update.message.reply_text(
            "⚠️ *Could not read all fields!*\n\n"
            "Please make sure you include all four fields:\n"
            "• NAME:\n• JOB:\n• COMPANY:\n• SKILLS:",
            parse_mode="Markdown",
        )
        return

    thinking_msg = await update.message.reply_text(get_thinking_message("coverletter"))
    result = await generate_cover_letter(name, job, company, skills)
    await thinking_msg.delete()

    save_analysis(
        user_id=user.id,
        username=user.username or user.first_name,
        action="coverletter",
        input_text=f"{name} | {job} | {company}",
        result_text=result,
    )

    chunks = split_message(f"✍️ *Cover Letter for {job} at {company}*\n━━━━━━━━━━━━━━━━━━━━━\n\n" + result)
    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode="Markdown")

    context.user_data.pop("mode", None)
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *Cover letter ready!* Copy it above and personalise as needed.\n\n"
        "💡 *Next step:* Use /interview to prepare for the interview!",
        parse_mode="Markdown",
    )
