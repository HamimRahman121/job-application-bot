"""
AI Service — Handles all Groq API interactions
Uses LLaMA 3.3 70B model (free & powerful)
"""

import asyncio
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL


client = Groq(api_key=GROQ_API_KEY)


def _ask_ai_sync(system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
    """
    Synchronous Groq API call — run inside asyncio.to_thread() to avoid blocking.
    """
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message},
            ],
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}\n\nPlease try again in a moment."


async def ask_ai(system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
    """
    Async wrapper — runs the blocking Groq call in a thread pool so the
    bot event loop stays responsive.
    """
    return await asyncio.to_thread(_ask_ai_sync, system_prompt, user_message, temperature)


# ── Prompt helpers ────────────────────────────────────────────────────────────

async def analyze_cv(cv_text: str) -> str:
    system = (
        "You are an expert career coach and professional CV reviewer with 15+ years of "
        "experience in HR and recruitment. Analyze the provided CV and give structured, "
        "actionable feedback. Be honest but encouraging. Use emojis to make the response "
        "readable in Telegram."
    )
    user = f"""Please analyze this CV and provide:

1. ✅ STRENGTHS (what's good)
2. ❌ WEAKNESSES (what's missing or weak)
3. 🔧 IMPROVEMENTS (specific actions to take)
4. ⭐ OVERALL SCORE (out of 10 with explanation)

CV Text:
\"\"\"
{cv_text}
\"\"\"
"""
    return await ask_ai(system, user, temperature=0.5)


async def match_cv_to_job(cv_text: str, job_description: str) -> str:
    system = (
        "You are an expert ATS (Applicant Tracking System) analyst and recruitment "
        "specialist. Compare CVs against job descriptions and give detailed match analysis. "
        "Use emojis to make the response easy to read on Telegram."
    )
    user = f"""Compare this CV to the Job Description and provide:

1. 🎯 MATCH SCORE (percentage, e.g. 72%)
2. ✅ MATCHING SKILLS & KEYWORDS
3. ❌ MISSING SKILLS & KEYWORDS
4. 📋 WHAT TO ADD to improve the match
5. 💡 ATS TIPS (how to optimize for automated screening)

CV:
\"\"\"
{cv_text}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"
"""
    return await ask_ai(system, user, temperature=0.4)


async def generate_cover_letter(name: str, job_title: str, company: str, skills: str) -> str:
    system = (
        "You are an expert career writer who crafts compelling, personalized cover letters "
        "that get interviews. Write professional, enthusiastic cover letters tailored to "
        "the specific role and company."
    )
    user = f"""Write a professional cover letter for:

Candidate Name: {name}
Job Title: {job_title}
Company: {company}
Key Skills & Experience: {skills}

Requirements:
- Professional and engaging tone
- 3-4 paragraphs
- Highlight relevant skills
- Show enthusiasm for the company
- Strong opening and closing
- Ready to copy-paste and send
"""
    return await ask_ai(system, user, temperature=0.7)


async def get_interview_questions(job_role: str) -> str:
    system = (
        "You are an expert interview coach who has helped thousands of candidates land "
        "their dream jobs. Provide realistic, role-specific interview questions with "
        "sample answers. Use emojis to make it engaging on Telegram."
    )
    user = f"""Generate interview preparation for a {job_role} position:

Provide:
1. 🔥 TOP 5 TECHNICAL QUESTIONS (with brief sample answers)
2. 💬 TOP 3 BEHAVIORAL QUESTIONS (STAR method answers)
3. 🤔 2 TRICKY QUESTIONS to watch out for
4. ❓ 3 QUESTIONS to ask the interviewer
5. 💡 TOP TIPS for this specific role

Role: {job_role}
"""
    return await ask_ai(system, user, temperature=0.6)


async def get_job_tips(topic: str = "general") -> str:
    system = (
        "You are a top career coach who gives practical, modern job hunting advice. "
        "Your tips are specific, actionable, and based on what actually works in today's "
        "job market. Use emojis for easy reading on Telegram."
    )
    user = f"""Give me the best job hunting tips for: {topic}

Include:
1. 🎯 QUICK WINS (things to do today)
2. 📅 WEEKLY STRATEGY
3. 🔗 NETWORKING TIPS
4. ⚠️ COMMON MISTAKES to avoid
5. 🚀 POWER MOVES that most people miss
"""
    return await ask_ai(system, user, temperature=0.6)


async def improve_linkedin(profile_text: str) -> str:
    system = (
        "You are a LinkedIn expert who helps professionals optimize their profiles "
        "for maximum visibility and recruiter attention. Give specific, actionable "
        "improvements using emojis for Telegram readability."
    )
    user = f"""Review and improve this LinkedIn profile section:

\"\"\"
{profile_text}
\"\"\"

Provide:
1. 📝 REWRITTEN VERSION (improved text)
2. 🔑 KEYWORDS to add for SEO
3. ✨ PROFILE TIPS specific to this content
4. 📊 VISIBILITY SCORE (out of 10)
"""
    return await ask_ai(system, user, temperature=0.6)
