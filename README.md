# 💼 Job Application Helper Bot

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-F55036?style=for-the-badge&logo=meta&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> An AI-powered Telegram bot that helps job seekers write better CVs, match job descriptions, generate cover letters, and prepare for interviews — all for **free**!

---

## ✨ Features

| Command | Description |
|---------|-------------|
| 📄 `/analyze` | Get expert AI feedback on your CV |
| 🎯 `/match` | Score your CV against any job description (ATS simulation) |
| ✍️ `/coverletter` | Generate a tailored professional cover letter |
| 🎤 `/interview` | Get role-specific interview questions + sample answers |
| 🔗 `/linkedin` | Optimise your LinkedIn profile section |
| 💡 `/tips` | Get personalised job hunting strategies |
| 📜 `/history` | Review your past analyses |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `python-telegram-bot` | Telegram Bot Framework (v21) |
| `groq` | Free AI API — LLaMA 3.3 70B model |
| `sqlite3` | Local database (built into Python) |
| `python-dotenv` | Secure environment variable management |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A Telegram account
- A free [Groq API key](https://console.groq.com)

### Step 1 — Get Your Bot Token
1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts — you'll get a **Bot Token**

### Step 2 — Get Your Free Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google (no credit card needed!)
3. Click **"Create API Key"** → copy the key

### Step 3 — Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/job-application-bot.git
cd job-application-bot

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Step 4 — Configure Environment
```bash
# Copy the template
copy .env.example .env   # Windows
# cp .env.example .env   # Mac/Linux

# Edit .env and add your keys
TELEGRAM_BOT_TOKEN=your_bot_token_here
GROQ_API_KEY=your_groq_key_here
```

### Step 5 — Run!
```bash
python main.py
```

Your bot is now **LIVE**! Open Telegram, find your bot, and send `/start` 🎉

---

## 📁 Project Structure

```
job-application-bot/
│
├── bot/
│   ├── handlers/              # One file per command
│   │   ├── start.py           # /start, /help, inline keyboard
│   │   ├── analyze.py         # /analyze — CV analysis
│   │   ├── match.py           # /match — CV vs Job Description
│   │   ├── coverletter.py     # /coverletter — cover letter
│   │   ├── interview.py       # /interview — interview prep
│   │   ├── tips.py            # /tips — job hunting advice
│   │   ├── linkedin.py        # /linkedin — profile optimiser
│   │   ├── history.py         # /history — past analyses
│   │   └── message_router.py  # Routes text messages by mode
│   │
│   ├── services/
│   │   ├── ai_service.py      # All Groq AI interactions
│   │   └── database.py        # SQLite CRUD operations
│   │
│   └── utils/
│       └── helpers.py         # Message splitting, formatting
│
├── config.py                  # App-wide settings
├── main.py                    # Entry point — registers all handlers
├── requirements.txt
├── .env.example               # Template — safe to commit
├── .gitignore
└── README.md
```

---

## 🌐 Deploy for Free (24/7)

### Option A — Railway (Recommended)
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) → "New Project" → "Deploy from GitHub"
3. Add your environment variables (`TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`)
4. Deploy! ✅ Free tier: 500 hrs/month

### Option B — Render
1. Go to [render.com](https://render.com)
2. New → Web Service → Connect your GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `python main.py`
5. Add environment variables → Deploy!

---

## 🤖 AI Model

This bot uses **LLaMA 3.3 70B** via [Groq](https://groq.com), which provides:
- ⚡ Extremely fast inference (fastest free AI API)
- 🧠 GPT-4 level quality
- 💸 Generous free tier (no credit card required)
- 🔒 Privacy-focused

---

## 📈 Future Enhancements

- [ ] PDF CV upload support (extract text from PDF)
- [ ] Job scraping from LinkedIn/Indeed
- [ ] Multi-language support
- [ ] Salary research feature
- [ ] Weekly job application tracker

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built with ❤️ using Python, python-telegram-bot, and Groq AI.

*If this helped you, please ⭐ star the repo!*
