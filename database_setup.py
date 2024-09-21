# database_setup.py
import sqlite3
from utils import hash_password, encrypt_data
import os

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create users table without DEFAULT ?
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        balance BLOB NOT NULL,
        is_admin INTEGER DEFAULT 0,
        failed_attempts INTEGER DEFAULT 0,
        locked_until INTEGER DEFAULT NULL
    )
    ''')

    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_sample_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        # Add a regular user
        cursor.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, ?)',
                       ('john_doe', hash_password('Password123!'), encrypt_data(1000.0)))
        # Add an admin user
        cursor.execute('INSERT INTO users (username, password, balance, is_admin) VALUES (?, ?, ?, ?)',
                       ('admin', hash_password('AdminPass123!'), encrypt_data(0.0), 1))
        conn.commit()
        print("Sample users added successfully.")
    except sqlite3.IntegrityError:
        print("Sample users already exist.")
    finally:
        conn.close()

if __name__ == "__main__":
    # Ensure the encryption key is set
    if not os.environ.get('APP_ENCRYPTION_KEY'):
        print("Please set the APP_ENCRYPTION_KEY environment variable before running this script.")
        exit(1)
    create_tables()
    add_sample_users()
    print("Database setup complete.")
