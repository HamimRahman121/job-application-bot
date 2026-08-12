"""
Database Service — SQLite storage for user history
Stores all analyses so users can review them later
"""

import sqlite3
from datetime import datetime
from config import DATABASE_PATH


def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            username    TEXT,
            action      TEXT NOT NULL,
            input_text  TEXT,
            result_text TEXT,
            created_at  TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_analysis(user_id: int, username: str, action: str, input_text: str, result_text: str):
    """Save an analysis result to the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses (user_id, username, action, input_text, result_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, action, input_text[:500], result_text[:1000],
          datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()


def get_user_history(user_id: int, limit: int = 5) -> list:
    """Fetch the last N analyses for a user."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT action, created_at, result_text
        FROM analyses
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_total_users() -> int:
    """Count unique users (for stats)."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM analyses")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_total_analyses() -> int:
    """Count total analyses performed."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM analyses")
    count = cursor.fetchone()[0]
    conn.close()
    return count
