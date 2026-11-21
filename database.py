import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "interview.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            total_score INTEGER NOT NULL,
            max_score INTEGER NOT NULL,
            percentage REAL NOT NULL,
            time_taken INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_number INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            score INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            time_taken INTEGER NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    """)
    conn.commit()
    conn.close()


def save_session(category, difficulty, total_questions, total_score, max_score, percentage, time_taken, qa_list):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (category, difficulty, total_questions, total_score, max_score, percentage, time_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (category, difficulty, total_questions, total_score, max_score, percentage, time_taken))
    session_id = cursor.lastrowid

    for qa in qa_list:
        cursor.execute("""
            INSERT INTO answers (session_id, question_number, question, answer, score, feedback, time_taken)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, qa["number"], qa["question"], qa["answer"], qa["score"], qa["feedback"], qa["time_taken"]))

    conn.commit()
    conn.close()
    return session_id


def get_all_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_session_answers(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM answers WHERE session_id = ? ORDER BY question_number", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM sessions")
    total_sessions = cursor.fetchone()["total"]
    cursor.execute("SELECT AVG(percentage) as avg FROM sessions")
    row = cursor.fetchone()
    avg_percentage = row["avg"] if row["avg"] is not None else 0
    cursor.execute("SELECT AVG(total_score * 1.0 / max_score) as ratio FROM sessions")
    row = cursor.fetchone()
    avg_ratio = row["ratio"] if row["ratio"] is not None else 0
    conn.close()
    return {
        "total_sessions": total_sessions,
        "avg_percentage": round(avg_percentage, 1),
        "avg_ratio": round(avg_ratio, 3),
    }


def delete_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM answers WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()


init_db()
