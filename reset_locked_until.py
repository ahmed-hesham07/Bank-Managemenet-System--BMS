# reset_locked_until.py
import sqlite3

def reset_locked_until():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET locked_until = NULL WHERE locked_until IS NOT NULL')
    conn.commit()
    conn.close()
    print("All users' 'locked_until' fields have been reset to NULL.")

if __name__ == "__main__":
    reset_locked_until()
