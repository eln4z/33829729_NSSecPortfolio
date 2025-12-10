import bcrypt, hashlib
from password_strength import password_strength
from twofactor import generate_2fa_secret
import pyotp

class AuthSystem:
    def __init__(self):
        self.users = {}

    def register(self, username: str, password: str):
        score, entropy = password_strength(password)
        if score < 5:
            return False, f"Password too weak (score {score}, entropy {entropy} bits)."

        bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        secret, qr_file = generate_2fa_secret(username)
        self.users[username] = {"hash": bcrypt_hash, "secret": secret}

        return True, f"User created. Scan QR in {qr_file}!"

    def login(self, username: str, password: str, token: str):
        user = self.users.get(username)
        if not user:
            return False, "User not found."

        stored_hash = user["hash"].encode()

        if not bcrypt.checkpw(password.encode(), stored_hash):
            return False, "Invalid password."

        totp = pyotp.TOTP(user["secret"])
        if not totp.verify(token):
            return False, "Invalid 2FA code."

        return True, "Login successful!"
