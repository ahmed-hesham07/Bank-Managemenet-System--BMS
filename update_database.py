# update_database.py
import sqlite3

def update_users_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Add 'failed_attempts' column if it doesn't exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'failed_attempts' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0')
        print("'failed_attempts' column added.")

    # Add 'locked_until' column if it doesn't exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'locked_until' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN locked_until INTEGER DEFAULT NULL')
        print("'locked_until' column added.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_users_table()
