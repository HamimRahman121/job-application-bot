import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token from @BotFather
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Groq API Key (free at console.groq.com)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Groq Model (free, fast, powerful)
GROQ_MODEL = "llama-3.3-70b-versatile"

# SQLite database file
DATABASE_PATH = "job_bot.db"

# Max message length for Telegram (4096 chars)
MAX_MESSAGE_LENGTH = 4000

# Bot version
BOT_VERSION = "1.0.0"
