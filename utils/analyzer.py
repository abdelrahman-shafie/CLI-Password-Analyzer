import string
from utils.entropy import calculate_entropy

def load_breached_list():
    try:
        with open('breached_passwords.txt', 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def load_dictionary_words():
    try:
        with open('dictionary_words.txt', 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def load_common_patterns():
    try:
        with open('common_patterns.txt', 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

BREACHED = load_breached_list()
DICTIONARY = load_dictionary_words()
PATTERNS = load_common_patterns()

def find_matches(password, word_list):
    matches = []
    for word in word_list:
        if word.lower() in password.lower():
            matches.append((word, password.lower().find(word.lower())))
    return matches

def analyze_password(password: str):
    # Scoring initialization
    length_score = 0
    complexity_score = 0

    # Check for length
    if len(password) >= 12:
        length_score = 40  # Full points for 12 or more characters
    elif len(password) >= 8:
        length_score = 20  # Partial points for 8-11 characters

    # Check complexity components
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    if has_upper:
        complexity_score += 10
    if has_lower:
        complexity_score += 10
    if has_digit:
        complexity_score += 10
    if has_special:
        complexity_score += 20

    # Detect breached passwords, dictionary words, and patterns
    breached_matches = find_matches(password, BREACHED)
    dictionary_matches = find_matches(password, DICTIONARY)
    pattern_matches = find_matches(password, PATTERNS)

    # Calculate penalties
    breached_penalty = 50 if breached_matches else 0
    dictionary_penalty = 30 if dictionary_matches else 0
    pattern_penalty = 25 if pattern_matches else 0

    # Calculate entropy
    password_entropy = calculate_entropy(password)
    entropy_score = min(int(password_entropy / 2), 30)  # Scaled entropy contribution

    # Combine scores
    raw_score = length_score + complexity_score + entropy_score - breached_penalty - dictionary_penalty - pattern_penalty
    score = max(min(raw_score, 100), 0)

    # Final score cap: Only passwords meeting all criteria can score 100
    if len(password) < 12 or not (has_upper and has_lower and has_digit and has_special):
        score = min(score, 95)

    # Recommendations
    recommendations = []
    if len(password) < 12:
        recommendations.append("Increase the length of your password to at least 12 characters.")
    if not has_upper:
        recommendations.append("Add uppercase letters.")
    if not has_lower:
        recommendations.append("Add lowercase letters.")
    if not has_digit:
        recommendations.append("Add digits.")
    if not has_special:
        recommendations.append("Add special characters.")

    if breached_matches:
        for match, position in breached_matches:
            recommendations.append(f"A breached password '{match}' was detected. Avoid using it.")
    if dictionary_matches:
        for match, position in dictionary_matches:
            recommendations.append(f"A dictionary word '{match}' was detected. Avoid using it.")
    if pattern_matches:
        for match, position in pattern_matches:
            recommendations.append(f"A common pattern '{match}' was detected. Avoid using it.")

    if not recommendations:
        recommendations = ["Your password meets all requirements."]

    return {
        'score': score,
        'recommendations': recommendations
    }
