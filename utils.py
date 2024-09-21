# utils.py
import hashlib
import os
import re
from cryptography.fernet import Fernet
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def is_strong_password(password):
    """
    Validates the strength of the password.
    Criteria:
    - At least 8 characters
    - Contains uppercase letters
    - Contains lowercase letters
    - Contains digits
    - Contains special characters
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def hash_password(password):
    """Hash a password with a randomly generated salt."""
    salt = os.urandom(16)  # 16-byte salt
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + pwd_hash  # Store salt + hash together

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    salt = stored_password[:16]
    stored_hash = stored_password[16:]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return pwd_hash == stored_hash

# Encryption utilities
def load_key():
    """Load the encryption key from the environment variable."""
    key = os.environ.get('APP_ENCRYPTION_KEY')
    if not key:
        raise EnvironmentError("APP_ENCRYPTION_KEY environment variable not set.")
    return key.encode()

fernet = Fernet(load_key())

def encrypt_data(data):
    """Encrypt data using Fernet symmetric encryption."""
    if isinstance(data, float):
        data = f"{data:.2f}"
    elif isinstance(data, int):
        data = str(data)
    elif isinstance(data, str):
        pass
    else:
        data = str(data)
    return fernet.encrypt(data.encode())

def decrypt_data(token):
    """Decrypt data using Fernet symmetric encryption."""
    return fernet.decrypt(token).decode()
