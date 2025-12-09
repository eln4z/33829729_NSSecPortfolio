import hashlib

COMMON_PASSWORDS = ["password", "123456", "12345678", "qwerty", "admin", "letmein"]

def brute_force_demo(target_hash: str, algo: str = "sha256"):
    tries = 0
    for pwd in COMMON_PASSWORDS:
        tries += 1
        b = pwd.encode()
        h = hashlib.md5(b).hexdigest() if algo.lower() == "md5" else hashlib.sha256(b).hexdigest()
        if h == target_hash:
            return True, pwd, tries
    return False, None, tries
