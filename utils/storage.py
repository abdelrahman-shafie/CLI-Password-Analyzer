import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import os
import json
from datetime import datetime, timezone

STORAGE_FILE = "password_store.enc"

# Derive key from master password
def derive_key_from_master(master_password: str, salt=b'static_salt', iterations=100_000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode('utf-8')))
    return key

# Store password function
def store_password(password: str, master_password: str):
    """
    Encrypts and stores a password in the local encrypted storage file.
    Ensures the master password matches the stored hash.
    """
    key = derive_key_from_master(master_password)
    f = Fernet(key)

    # Check if the master password matches the existing one
    if os.path.exists(STORAGE_FILE):
        existing_passwords = retrieve_passwords(master_password, raise_exception=False)
        if existing_passwords is None:
            raise ValueError("Master password mismatch or storage is corrupted.")

    # Append a new password record with timestamp
    record = {
        "password": password,
        "stored_at": datetime.now(timezone.utc).isoformat()
    }
    if os.path.exists(STORAGE_FILE):
        passwords = retrieve_passwords(master_password, raise_exception=False)
    else:
        passwords = []

    passwords.append(record)
    data = json.dumps(passwords).encode('utf-8')
    encrypted = f.encrypt(data)

    with open(STORAGE_FILE, 'wb') as fp:
        fp.write(encrypted)


# Retrieve passwords function
def retrieve_passwords(master_password: str, raise_exception=True):
    """
    Decrypts and retrieves the list of stored passwords.
    """
    if not os.path.exists(STORAGE_FILE):
        return []

    key = derive_key_from_master(master_password)
    f = Fernet(key)

    try:
        with open(STORAGE_FILE, 'rb') as fp:
            encrypted = fp.read()
        data = f.decrypt(encrypted)
        return json.loads(data.decode('utf-8'))
    except Exception:
        if raise_exception:
            raise ValueError("Incorrect master password or storage corrupted.")
        else:
            return None

