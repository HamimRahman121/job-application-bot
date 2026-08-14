"""
Helper utilities — message splitting, formatting, etc.
"""

from config import MAX_MESSAGE_LENGTH


def split_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """
    Split long AI responses into Telegram-safe chunks (max 4096 chars).
    Tries to split at newlines to keep formatting clean.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    while len(text) > max_length:
        # Find last newline within the limit
        split_at = text.rfind("\n", 0, max_length)
        if split_at == -1:
            split_at = max_length
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    if text:
        chunks.append(text)
    return chunks


def format_history_entry(action: str, created_at: str, result_preview: str) -> str:
    """Format a single history entry for display."""
    action_emoji = {
        "analyze":       "📄 CV Analysis",
        "match":         "🎯 Job Match",
        "coverletter":   "✍️ Cover Letter",
        "interview":     "🎤 Interview Prep",
        "tips":          "💡 Job Tips",
        "linkedin":      "🔗 LinkedIn Optimiser",
    }.get(action, f"🤖 {action.title()}")

    preview = result_preview[:120].replace("\n", " ") + "..."
    return f"*{action_emoji}*\n🕐 {created_at}\n_{preview}_"


def get_thinking_message(action: str) -> str:
    """Return a 'thinking' message appropriate to the action."""
    messages = {
        "analyze":     "📄 Analysing your CV... please wait ⏳",
        "match":       "🎯 Matching your CV to the job description... ⏳",
        "coverletter": "✍️ Writing your cover letter... ⏳",
        "interview":   "🎤 Preparing your interview guide... ⏳",
        "tips":        "💡 Gathering the best career tips... ⏳",
        "linkedin":    "🔗 Optimising your LinkedIn profile... ⏳",
    }
    return messages.get(action, "🤖 AI is thinking... please wait ⏳")
