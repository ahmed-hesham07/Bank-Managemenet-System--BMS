# add_admin.py
import sqlite3
from utils import hash_password, encrypt_data
import os

def add_admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        admin_username = 'admin'
        admin_password = 'AdminPass123!'  # Choose a strong password
        cursor.execute('INSERT INTO users (username, password, balance, is_admin) VALUES (?, ?, ?, ?)',
                       (admin_username, hash_password(admin_password), encrypt_data(0.0), 1))
        conn.commit()
        print("Admin user created successfully.")
    except sqlite3.IntegrityError:
        print("Admin user already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    # Ensure the encryption key is set
    if not os.environ.get('APP_ENCRYPTION_KEY'):
        print("Please set the APP_ENCRYPTION_KEY environment variable before running this script.")
        exit(1)
    add_admin()
