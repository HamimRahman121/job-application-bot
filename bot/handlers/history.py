"""
/history command — View past analyses
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.services.database import get_user_history, get_total_users, get_total_analyses
from bot.utils.helpers import format_history_entry


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /history command."""
    await _show_history(update.effective_user.id, update.message.reply_text)


async def show_history_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show history from inline keyboard button."""
    query = update.callback_query
    await _show_history(query.from_user.id, query.message.reply_text)


async def _show_history(user_id: int, reply_fn):
    """Shared logic for showing history."""
    rows = get_user_history(user_id, limit=5)

    if not rows:
        await reply_fn(
            "📜 *Your Analysis History*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
            "You haven't used any features yet!\n\n"
            "Get started with:\n"
            "• /analyze — Analyse your CV\n"
            "• /match — Match to a job\n"
            "• /coverletter — Write a cover letter",
            parse_mode="Markdown",
        )
        return

    lines = ["📜 *Your Last 5 Analyses*\n━━━━━━━━━━━━━━━━━━━━━\n"]
    for i, (action, created_at, result_preview) in enumerate(rows, 1):
        entry = format_history_entry(action, created_at, result_preview or "")
        lines.append(f"*{i}.* {entry}")
        lines.append("─────────────────────")

    await reply_fn("\n".join(lines), parse_mode="Markdown")
