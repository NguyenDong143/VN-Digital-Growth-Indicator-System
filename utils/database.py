"""
SQLite database module for user authentication.
Replaces CSV-based storage for better security and concurrent access.
"""

import warnings
warnings.filterwarnings('ignore')

import sqlite3
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path("data/db/users.db")


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
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
        # Bật WAL mode để hỗ trợ concurrent read/write tốt hơn
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'province',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                failed_attempts INTEGER DEFAULT 0,
                last_failed_at TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                target TEXT,
                details TEXT
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_log(actor)')
        conn.commit()


def get_user(username: str) -> dict | None:
    """
    Get user by username.

    Returns
    -------
    dict or None
        User data với keys: id, username, password, role, created_at,
        failed_attempts, last_failed_at.
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
        True nếu thành công, False nếu username đã tồn tại.
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
        cursor.execute(
            "SELECT id, username, role, created_at, failed_attempts "
            "FROM users ORDER BY id"
        )
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


# =========================================================
# RATE LIMITING HELPERS
# =========================================================

def register_login_failure(username: str) -> None:
    """Tăng failed_attempts và cập nhật last_failed_at cho user."""
    now = datetime.utcnow().isoformat(timespec="seconds")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET failed_attempts = COALESCE(failed_attempts, 0) + 1, "
            "last_failed_at = ? WHERE username = ?",
            (now, username),
        )
        conn.commit()


def reset_login_failures(username: str) -> None:
    """Reset failed_attempts sau khi đăng nhập thành công."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET failed_attempts = 0, last_failed_at = NULL "
            "WHERE username = ?",
            (username,),
        )
        conn.commit()


# =========================================================
# AUDIT LOG
# =========================================================

def log_audit(actor: str, action: str, target: str = None, details: str = None) -> None:
    """
    Ghi một entry vào audit_log.
    action nên là verb ngắn: 'login', 'login_failed', 'register', 'promote', 'delete'.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_log (actor, action, target, details) VALUES (?, ?, ?, ?)",
            (actor, action, target, details),
        )
        conn.commit()


def get_audit_log(limit: int = 200) -> list[dict]:
    """Lấy audit_log mới nhất (mặc định 200 dòng)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, actor, action, target, details "
            "FROM audit_log ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
