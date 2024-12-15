import string
import random
import pyperclip
import threading
import time
from colorama import init, Fore, Style

def clear_clipboard_after_delay(delay: int):
    """Clears the clipboard after a specified delay (in seconds)."""
    time.sleep(delay)
    pyperclip.copy("")  # Clear clipboard

def generate_strong_password():
    """
    Generates a strong password, copies it to the clipboard,
    and clears the clipboard asynchronously after 30 seconds.
    """
    length = 16
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    secure_random = random.SystemRandom()
    password = ''.join(secure_random.choice(charset) for _ in range(length))

    # Copy password to clipboard
    try:
        pyperclip.copy(password)
        print(Fore.GREEN + "Password has been securely copied to the clipboard!")
        print(Fore.YELLOW + "It will be cleared in 30 seconds.")
        # Start a thread to clear the clipboard after 30 seconds
        threading.Thread(target=clear_clipboard_after_delay, args=(30,), daemon=True).start()
    except Exception as e:
        print("Failed to copy password to clipboard:", e)

    return password
