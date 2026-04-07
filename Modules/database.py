import sqlite3
import os

# Single source of truth for DB path
DB_PATH = os.path.join(os.path.dirname(__file__), "office_systems.db")


def log_action(user_id, action):
    """Log an action performed by a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (user_id, action) VALUES (?, ?)",
        (user_id, action)
    )
    conn.commit()
    conn.close()


def approve_user(username):
    """Approve a pending user by username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_approved = 1 WHERE username = ?",
        (username,)
    )
    conn.commit()
    conn.close()


def get_pending_users():
    """Return all users who are not yet approved."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE is_approved = 0")
    users = cursor.fetchall()
    conn.close()
    return users


def get_logs_by_user(user_id):
    """Return all logs for a given user ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT action, timestamp FROM logs WHERE user_id = ?",
        (user_id,)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs


def get_logs_by_date(date):
    """Return all logs for a given date (YYYY-MM-DD)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, action, timestamp FROM logs WHERE date(timestamp) = ?",
        (date,)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs


def assign_role(username, role):
    """Assign a role to a user by username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (role, username)
    )
    conn.commit()
    conn.close()


def get_all_users():
    """Return all users with their id, username, role, and approval status."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, is_approved FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def delete_user(username):
    """Delete a user by username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def get_dashboard_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_approved = 0")
    pending_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_logs = cursor.fetchone()[0]
    cursor.execute("SELECT user_id, action, timestamp FROM logs ORDER BY timestamp DESC LIMIT 8")
    recent_logs = cursor.fetchall()
    conn.close()
    return {
        "total_users": total_users,
        "pending_users": pending_users,
        "total_logs": total_logs,
        "recent_logs": recent_logs,
    }

def get_all_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, action, timestamp FROM logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return logs


#admin
#admin123

#roy
#roy123

#evie
#evie123

#ray
#ray123