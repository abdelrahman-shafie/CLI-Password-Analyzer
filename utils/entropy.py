import math
import string

def calculate_entropy(password: str) -> float:
    # Determine character set size
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    if charset == 0:
        # If no character set detected, entropy is zero
        return 0.0

    # Entropy calculation: length * log2(charset)
    return len(password) * math.log2(charset)
