import bcrypt
from Modules.database import log_action, DB_PATH
import sqlite3


def user_exists(username):
    """Check if a user with the given username already exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def hash_password(password):
    """Hash a plain-text password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def register_user(username, password):
    """
    Register a new user with a hashed password.
    Returns True on success, False if username already exists.
    """
    if user_exists(username):
        return False

    hashed_password = hash_password(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role, is_approved) VALUES (?, ?, ?, ?)",
        (username, hashed_password, "officer", 0)
    )
    conn.commit()
    conn.close()

    log_action(None, f"REGISTERED_{username}")
    return True


def register():
    """Interactive registration prompt for the CLI."""
    username = input("Enter new username: ").strip()
    password = input("Enter password: ").strip()

    if register_user(username, password):
        print("Registration successful! Please wait for admin approval.")
    else:
        print("Username already exists. Please try a different one.")


def get_user(username):
    """Fetch a user row by username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def login_user(username, password):
    """
    Attempt to log in a user.
    Returns the user row if credentials are correct and account is approved.
    Returns None otherwise.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        print("User not found.")
        return None

    stored_hash = user[2]

    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')

    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        print("Incorrect password.")
        return None

    if user[4] == 0:
        print("Account not yet approved by admin.")
        return None

    return user