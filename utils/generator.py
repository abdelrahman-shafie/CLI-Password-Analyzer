import string
import random


def generate_strong_password():
    length = 16
    # Include a mix of character sets
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    # Use SystemRandom for better randomness
    secure_random = random.SystemRandom()

    # Generate the password
    password = ''.join(secure_random.choice(charset) for _ in range(length))
    return password
