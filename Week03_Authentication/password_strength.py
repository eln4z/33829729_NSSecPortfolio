import string, math

COMMON_PASSWORDS = ["password", "123456", "12345678", "qwerty", "admin", "letmein"]

def password_strength(pwd: str):
    score = 0
    pool = 0

    if len(pwd) >= 8: score += 1
    if len(pwd) >= 12: score += 1

    if any(c.islower() for c in pwd):
        pool += 26; score += 1
    if any(c.isupper() for c in pwd):
        pool += 26; score += 1
    if any(c.isdigit() for c in pwd):
        pool += 10; score += 1
    if any(c in string.punctuation for c in pwd):
        pool += len(string.punctuation); score += 1

    if pwd.lower() in COMMON_PASSWORDS:
        score = 0

    entropy = len(pwd) * math.log2(pool) if pool > 0 else 0.0
    return score, round(entropy, 2)
