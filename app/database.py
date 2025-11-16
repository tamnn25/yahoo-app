import sqlite3
from app.config import DB_FILE
from datetime import date

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    add_column_if_not_exists("users", "token", "TEXT")
    add_column_if_not_exists("users", "password", "TEXT")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        token TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS friends (
        user_id INTEGER NOT NULL,
        friend_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, friend_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(friend_id) REFERENCES users(id)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")

    # Chats table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp TEXT,
        day TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_column_if_not_exists(table: str, column: str, col_type: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # check if column already exists
    cur.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cur.fetchall()]

    if column not in columns:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        conn.commit()
        print(f"✅ Added column '{column}' to table '{table}'.")
    else:
        print(f"ℹ️ Column '{column}' already exists in table '{table}'.")

    conn.close()

def save_message(username, message):
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    cursor.execute(
        "INSERT INTO chats (username, message, timestamp, day) VALUES (?, ?, datetime('now'), ?)",
        (username, message, today)
    )
    conn.commit()
    conn.close()

def load_messages_for_today():
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    cursor.execute("SELECT * FROM chats WHERE day = ? ORDER BY timestamp ASC", (today,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]