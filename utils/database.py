"""
SQLite database module for user authentication.
Replaces CSV-based storage for better security and concurrent access.
"""

import warnings
warnings.filterwarnings('ignore')

import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path("data/db/users.db")


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the database and create tables if they don't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'province',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


def get_user(username: str) -> dict | None:
    """
    Get user by username.
    
    Returns
    -------
    dict or None
        User data with keys: id, username, password, role, created_at
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", 
            (username,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def add_user(username: str, password_hash: str, role: str = "province") -> bool:
    """
    Add a new user to the database.
    
    Returns
    -------
    bool
        True if successful, False if username already exists.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def get_all_users() -> list[dict]:
    """Get all users from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, created_at FROM users")
        return [dict(row) for row in cursor.fetchall()]


def delete_user(username: str) -> bool:
    """Delete a user by username."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cursor.rowcount > 0


def update_user_role(username: str, new_role: str) -> bool:
    """Update user's role."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET role = ? WHERE username = ?",
            (new_role, username)
        )
        conn.commit()
        return cursor.rowcount > 0


def update_user_password(username: str, new_password_hash: str) -> bool:
    """Update user's password (expects hashed password)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password_hash, username)
        )
        conn.commit()
        return cursor.rowcount > 0
