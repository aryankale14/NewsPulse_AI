import sqlite3
import json
import os
import logging

DB_FILE = os.getenv("DB_PATH", "subscribers.db")
OLD_JSON_FILE = "subscribers.json"
logger = logging.getLogger(__name__)

def get_connection():
    # SQLite can be used safely across threads if check_same_thread=False
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    """Initializes the SQLite database and migrates existing JSON data if present."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chat_id TEXT PRIMARY KEY,
                categories TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

    # Automatic Migration Script
    if os.path.exists(OLD_JSON_FILE):
        try:
            with open(OLD_JSON_FILE, "r") as f:
                old_data = json.load(f)
            
            logger.info(f"Found {OLD_JSON_FILE}. Migrating {len(old_data)} users to SQLite database...")
            
            with get_connection() as conn:
                cursor = conn.cursor()
                for chat_id, cats in old_data.items():
                    cats_json = json.dumps(cats)
                    cursor.execute('''
                        INSERT OR REPLACE INTO users (chat_id, categories)
                        VALUES (?, ?)
                    ''', (chat_id, cats_json))
                conn.commit()
                
            # Rename the old file so we don't migrate again
            os.rename(OLD_JSON_FILE, "subscribers.json.bak")
            logger.info("Migration successful! Old file renamed to subscribers.json.bak")
            
        except Exception as e:
            logger.error(f"Error migrating JSON data: {e}")

def get_all_users():
    """Returns a dictionary of all registered users and their categories. Format: {chat_id_str: [list_of_cats]}"""
    users = {}
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id, categories FROM users")
        for row in cursor.fetchall():
            chat_id = row[0]
            try:
                cats = json.loads(row[1])
                users[str(chat_id)] = cats
            except Exception:
                users[str(chat_id)] = []
    return users

def save_user_categories(chat_id: str, categories: list):
    """Adds a new user or updates an existing user's category preferences."""
    cats_json = json.dumps(categories)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (chat_id, categories)
            VALUES (?, ?)
        ''', (chat_id, cats_json))
        conn.commit()

def remove_user(chat_id: str):
    """Deletes a user from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))
        conn.commit()
