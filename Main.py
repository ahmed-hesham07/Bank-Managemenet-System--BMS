# main.py
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from utils import hash_password, verify_password, is_strong_password, encrypt_data, decrypt_data
import logging
import os
import time

# Configuration Constants
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes in seconds

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Banking App")
        self.root.geometry("500x500")
        self.current_user = None

        self.create_login_screen()


    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Online Banking Login", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.root, text="Username", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack()

        tk.Label(self.root, text="Password", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack()

        tk.Button(self.root, text="Login", width=15, command=self.login, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Register", width=15, command=self.create_registration_screen, font=("Arial", 12)).pack(pady=5)


    def create_registration_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Register New Account", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.root, text="Username", font=("Arial", 12)).pack(pady=5)
        self.reg_username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.reg_username_entry.pack()

        tk.Label(self.root, text="Password", font=("Arial", 12)).pack(pady=5)
        self.reg_password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.reg_password_entry.pack()

        tk.Label(self.root, text="Confirm Password", font=("Arial", 12)).pack(pady=5)
        self.reg_confirm_password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.reg_confirm_password_entry.pack()

        tk.Button(self.root, text="Register", width=15, command=self.register, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Back to Login", width=15, command=self.create_login_screen, font=("Arial", 12)).pack(pady=5)

    def register(self):
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if not is_strong_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and include uppercase letters, lowercase letters, numbers, and special characters.")
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, ?)',
                           (username, hash_password(password), encrypt_data(0.0)))
            conn.commit()
            logging.info(f"New user registered: '{username}'.")
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.create_login_screen()
        except sqlite3.IntegrityError:
            logging.warning(f"Registration attempt with existing username: '{username}'.")
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, password, balance, is_admin, failed_attempts, locked_until FROM users WHERE username=?',
            (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id, stored_password, encrypted_balance, is_admin, failed_attempts, locked_until = result

            current_time = int(time.time())

            # Check if the account is locked
            if locked_until is not None and locked_until > current_time:
                remaining = locked_until - current_time
                minutes, seconds = divmod(remaining, 60)
                messagebox.showerror("Account Locked",
                                     f"Account is locked. Try again in {minutes} minutes and {seconds} seconds.")
                logging.warning(f"Locked account login attempt for user '{username}'.")
                return

            if verify_password(stored_password, password):
                self.current_user = {
                    'id': user_id,
                    'username': username,
                    'balance': float(decrypt_data(encrypted_balance)),
                    'is_admin': is_admin
                }
                # Reset failed attempts
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id=?', (user_id,))
                conn.commit()
                conn.close()

                logging.info(f"User '{username}' logged in successfully.")

                if is_admin:
                    self.create_admin_dashboard()
                else:
                    self.create_user_dashboard()
            else:
                failed_attempts += 1
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                if failed_attempts >= MAX_FAILED_ATTEMPTS:
                    locked_until = int(time.time()) + LOCKOUT_DURATION
                    cursor.execute('UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id=?',
                                   (failed_attempts, locked_until, user_id))
                    conn.commit()
                    conn.close()
                    messagebox.showerror("Account Locked",
                                         "Too many failed attempts. Your account has been locked for 5 minutes.")
                    logging.warning(f"User '{username}' account locked due to multiple failed login attempts.")
                else:
                    cursor.execute('UPDATE users SET failed_attempts = ? WHERE id=?', (failed_attempts, user_id))
                    conn.commit()
                    conn.close()
                    attempts_left = MAX_FAILED_ATTEMPTS - failed_attempts
                    messagebox.showerror("Error",
                                         f"Invalid credentials. {attempts_left} attempts left before account lockout.")
                    logging.warning(f"Failed login attempt {failed_attempts} for user '{username}'.")
        else:
            messagebox.showerror("Error", "User not found.")
            logging.warning(f"Login attempt for non-existent user '{username}'.")

    def create_user_dashboard(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Welcome, {self.current_user['username']}", font=("Arial", 16)).pack(pady=20)
        self.balance_var = tk.StringVar()
        self.update_balance()
        tk.Label(self.root, textvariable=self.balance_var, font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Transfer Funds", width=20, command=self.transfer_funds, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Transaction History", width=20, command=self.transaction_history, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Logout", width=20, command=self.logout, font=("Arial", 12)).pack(pady=5)

    def create_admin_dashboard(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Admin Dashboard - {self.current_user['username']}", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="View All Users", width=20, command=self.view_all_users, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="View All Transactions", width=20, command=self.view_all_transactions, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Logout", width=20, command=self.logout, font=("Arial", 12)).pack(pady=5)

    def view_all_users(self):
        users_window = tk.Toplevel(self.root)
        users_window.title("All Users")
        users_window.geometry("600x400")

        tk.Label(users_window, text="All Registered Users", font=("Arial", 14)).pack(pady=10)

        columns = ("ID", "Username", "Balance", "Is Admin", "Failed Attempts", "Locked Until")
        tree = ttk.Treeview(users_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, balance, is_admin, failed_attempts, locked_until FROM users')
        users = cursor.fetchall()
        conn.close()

        for user in users:
            user_id, username, encrypted_balance, is_admin, failed_attempts, locked_until = user
            balance = float(decrypt_data(encrypted_balance))
            locked_until_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(locked_until)) if locked_until > 0 else "N/A"
            tree.insert('', tk.END, values=(
                user_id,
                username,
                f"${balance:.2f}",
                "Yes" if is_admin else "No",
                failed_attempts,
                locked_until_str
            ))

    def view_all_transactions(self):
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("All Transactions")
        transactions_window.geometry("700x500")

        tk.Label(transactions_window, text="All Transactions", font=("Arial", 14)).pack(pady=10)

        columns = ("ID", "User ID", "Type", "Amount", "Timestamp")
        tree = ttk.Treeview(transactions_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            if col == "Timestamp":
                tree.column(col, width=150, anchor=tk.CENTER)
            else:
                tree.column(col, width=100, anchor=tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, user_id, type, amount, timestamp FROM transactions ORDER BY timestamp DESC')
        transactions = cursor.fetchall()
        conn.close()

        for txn in transactions:
            tree.insert('', tk.END, values=txn)

    def update_balance(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE id=?', (self.current_user['id'],))
        encrypted_balance = cursor.fetchone()[0]
        conn.close()
        balance = float(decrypt_data(encrypted_balance))
        self.current_user['balance'] = balance
        self.balance_var.set(f"Current Balance: ${balance:.2f}")

    def transfer_funds(self):
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Transfer Funds")
        transfer_window.geometry("400x300")

        tk.Label(transfer_window, text="Transfer Funds", font=("Arial", 14)).pack(pady=10)

        tk.Label(transfer_window, text="Recipient Username", font=("Arial", 12)).pack(pady=5)
        recipient_entry = tk.Entry(transfer_window, font=("Arial", 12))
        recipient_entry.pack()

        tk.Label(transfer_window, text="Amount", font=("Arial", 12)).pack(pady=5)
        amount_entry = tk.Entry(transfer_window, font=("Arial", 12))
        amount_entry.pack()

        tk.Button(transfer_window, text="Send", command=lambda: self.perform_transfer(recipient_entry.get(), amount_entry.get(), transfer_window), font=("Arial", 12)).pack(pady=20)

    def perform_transfer(self, recipient, amount, window):
        recipient = recipient.strip()
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        if not recipient:
            messagebox.showerror("Error", "Please enter a recipient username.")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Transfer amount must be positive.")
            return

        if amount > self.current_user['balance']:
            messagebox.showerror("Error", "Insufficient funds.")
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if recipient exists
        cursor.execute('SELECT id, balance FROM users WHERE username=?', (recipient,))
        recipient_data = cursor.fetchone()
        if not recipient_data:
            messagebox.showerror("Error", "Recipient not found.")
            conn.close()
            return

        recipient_id, recipient_encrypted_balance = recipient_data
        recipient_balance = float(decrypt_data(recipient_encrypted_balance))

        try:
            # Begin transaction
            conn.execute('BEGIN')

            # Update sender's balance
            new_sender_balance = self.current_user['balance'] - amount
            cursor.execute('UPDATE users SET balance = ? WHERE id=?', (encrypt_data(new_sender_balance), self.current_user['id']))

            # Update recipient's balance
            new_recipient_balance = recipient_balance + amount
            cursor.execute('UPDATE users SET balance = ? WHERE id=?', (encrypt_data(new_recipient_balance), recipient_id))

            # Log transactions
            cursor.execute('INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)',
                           (self.current_user['id'], 'debit', amount))
            cursor.execute('INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)',
                           (recipient_id, 'credit', amount))

            conn.commit()
            logging.info(f"User '{self.current_user['username']}' transferred ${amount:.2f} to '{recipient}'.")
            messagebox.showinfo("Success", "Transfer completed successfully.")
            window.destroy()
            self.update_balance()
        except sqlite3.Error as e:
            conn.rollback()
            logging.error(f"Transfer error: {e}")
            messagebox.showerror("Error", "An unexpected error occurred during the transfer. Please try again.")
        finally:
            conn.close()

    def transaction_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Transaction History")
        history_window.geometry("600x500")

        tk.Label(history_window, text="Your Transaction History", font=("Arial", 14)).pack(pady=10)

        columns = ("Type", "Amount", "Timestamp")
        tree = ttk.Treeview(history_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor=tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT type, amount, timestamp FROM transactions WHERE user_id=? ORDER BY timestamp DESC',
                       (self.current_user['id'],))
        transactions = cursor.fetchall()
        conn.close()

        for txn in transactions:
            txn_type, amount, timestamp = txn
            tree.insert('', tk.END, values=(txn_type.capitalize(), f"${amount:.2f}", timestamp))

    def logout(self):
        logging.info(f"User '{self.current_user['username']}' logged out.")
        self.current_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Ensure the encryption key is set
    if not os.environ.get('APP_ENCRYPTION_KEY'):
        print("Please set the APP_ENCRYPTION_KEY environment variable before running the application.")
        exit(1)

    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
