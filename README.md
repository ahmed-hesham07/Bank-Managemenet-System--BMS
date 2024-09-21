# **Online Banking System**

An online banking system built using Python, Tkinter for the graphical user interface (GUI), and SQLite for data storage. This project provides basic banking functionality, including user registration, login, balance checking, transactions, and an admin panel. It also incorporates security features like password hashing, data encryption, account locking, and secure user authentication.

## **Features**

- **User Registration & Login**: Clients can register and log into their accounts.
- **Balance Check**: Users can view their current account balance.
- **Deposit & Withdrawal**: Clients can deposit and withdraw funds from their accounts.
- **Transaction History**: View the transaction history.
- **Admin Panel**: Admin can view user details and manage accounts.
- **Password Security**: Secure password hashing and strength validation.
- **Data Encryption**: User balances are encrypted to ensure sensitive information is protected.
- **Account Locking**: After multiple failed login attempts, the account is temporarily locked.

## **Security Features**

- **Password Hashing**: User passwords are securely hashed using the `bcrypt` library.
- **Data Encryption**: Sensitive data, such as account balance, is encrypted using `Fernet` symmetric encryption.
- **Environment Variables**: Encryption keys and other sensitive settings are stored as environment variables.
- **Account Locking**: Accounts are locked for a certain period after multiple failed login attempts to prevent brute-force attacks.
- **Password Strength Validation**: Passwords must meet certain strength criteria.

## **Installation**

### **1. Prerequisites**

- Python 3.x installed on your system.
- Libraries: `tkinter`, `sqlite3`, `bcrypt`, `cryptography`, `python-dotenv`.

### **2. Clone the Repository**

```bash
git clone https://github.com/yourusername/online-banking-system.git
cd online-banking-system
```

### **3. Install Dependencies**

Install the required Python packages using `pip`:

```bash
pip install bcrypt cryptography python-dotenv
```

### **4. Set Up Environment Variables**

Create a `.env` file in the project root directory:

```bash
touch .env
```

In the `.env` file, add the following:

```bash
APP_ENCRYPTION_KEY=your_encryption_key_here
```

Replace `your_encryption_key_here` with a securely generated key. You can generate a key using Python as follows:

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### **5. Set Up the Database**

Run the `database_setup.py` script to initialize the SQLite database and create the necessary tables:

```bash
python database_setup.py
```

This will also add two sample users:
- **Regular User**: Username: `john_doe`, Password: `Password123!`, Balance: `1000.0`
- **Admin User**: Username: `admin`, Password: `AdminPass123!`

### **6. Run the Application**

Once everything is set up, you can run the main application:

```bash
python Main.py
```

### **7. Admin Access**

To access the admin screen:
- Log in as the admin user (`admin`).
- Upon successful login, you’ll be presented with the admin panel.

## **Usage**

1. **Register a New User**: Create an account with a strong password.
2. **Login**: Use your credentials to log into your account.
3. **Check Balance**: View your account balance on the home screen.
4. **Deposit/Withdraw**: Perform transactions.
5. **View Transactions**: Check your transaction history in the account.

### **Admin Panel**

- **View Users**: See the list of registered users and their details.
- **Manage Accounts**: Admin can manage account balances and other settings.

## **Project Structure**

```
|-- database.db               # SQLite database file (created after running setup)
|-- Main.py                   # Main application file with Tkinter GUI
|-- database_setup.py          # Script to set up the SQLite database and sample users
|-- utils.py                  # Utility functions for hashing, encryption, and data handling
|-- README.md                 # Project documentation
|-- .env                      # Environment variables file (created by the user)
```

## **Contributing**

Contributions are welcome! Feel free to submit a pull request with any features, bug fixes, or improvements.

### **Future Features**
- Implement multi-factor authentication (MFA).
- Add email notifications for transactions.
- Enhance the admin panel with more management tools.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to modify this `README.md` to better suit your project as it evolves!