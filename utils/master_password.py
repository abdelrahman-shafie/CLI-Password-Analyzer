import os
import hashlib
from getpass import getpass

MASTER_PASSWORD_FILE = "master_password.hash"

def setup_master_password():
    """
    Sets up a new master password by hashing and storing it locally.
    """
    if os.path.exists(MASTER_PASSWORD_FILE):
        print("Master password is already set up.")
        return

    print("Setting up your master password. \n!! Make sure to remember it !!")
    master_password = getpass("Enter your master password: ").strip()
    confirm_password = getpass("Confirm your master password: ").strip()

    if master_password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    hashed_password = hashlib.sha256(master_password.encode('utf-8')).hexdigest()
    with open(MASTER_PASSWORD_FILE, 'w') as fp:
        fp.write(hashed_password)
    print("Master password has been set up successfully.")

def verify_master_password(input_password):
    """
    Verifies the provided master password against the stored hash.
    """
    if not os.path.exists(MASTER_PASSWORD_FILE):
        print("No master password is set up. Please run the setup first.")
        return False

    with open(MASTER_PASSWORD_FILE, 'r') as fp:
        stored_hash = fp.read().strip()

    input_hash = hashlib.sha256(input_password.encode('utf-8')).hexdigest()
    return input_hash == stored_hash
