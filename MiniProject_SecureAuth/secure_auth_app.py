"""
Mini Project: Secure Authentication System

Features:
- Entropy-based password policy (balanced usability)
- Argon2id password hashing (argon2-cffi)
- Account lockout after repeated failed attempts
- JSON-based user database
- JSON-based audit log

Run with:
    python secure_auth_app.py
"""

from __future__ import annotations

import json
import math
import string
from datetime import datetime, timedelta, timezone
from getpass import getpass
from pathlib import Path
from typing import Dict, Any

from argon2 import PasswordHasher, exceptions as argon2_exceptions


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

USERS_FILE = Path("auth_data.json")
LOG_FILE = Path("audit_log.json")

# Aliases for compatibility with demo script
DATA_FILE = USERS_FILE

LOCKOUT_THRESHOLD = 5          # Number of failed attempts before lockout
LOCKOUT_SECONDS = 300          # Lockout duration in seconds (5 minutes)

ph = PasswordHasher()          # Uses Argon2id by default


# ----------------------------------------------------------------------
# Time utilities
# ----------------------------------------------------------------------
def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def now_iso() -> str:
    return now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

# ----------------------------------------------------------------------
# Storage helpers
# ----------------------------------------------------------------------
def load_users() -> Dict[str, Any]:
    """
    Load users from the USERS_FILE (auth_data.json).
    Returns an empty dict if the file does not exist.
    """
    if not USERS_FILE.exists():
        return {}
    with USERS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_db() -> Dict[str, Any]:
    """
    Alias for load_users for compatibility with demo script.
    """
    return load_users()

def save_users(users: Dict[str, Any]) -> None:
    """
    Save users to the USERS_FILE (auth_data.json).
    """
    with USERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

# ----------------------------------------------------------------------
# Password policy
# ----------------------------------------------------------------------
COMMON_PASSWORDS = {
    "password", "123456", "123456789", "test1", "password1", "qwerty", "abc123", "letmein", "monkey", "dragon"
}

def estimate_entropy(password: str) -> float:
    """
    Estimate password entropy in bits.
    """
    if not password:
        return 0.0
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    if pool == 0:
        pool = 10
    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def password_is_acceptable(password: str) -> tuple[bool, str, float]:
    """
    Balanced policy:
    - Rejects very short or common passwords.
    - Uses entropy threshold rather than forcing all character types.
    Returns (is_ok, message, entropy_bits).
    """
    if len(password) < 8:
        return False, "Password is too short (minimum 8 characters).", 0.0
    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common and easily guessable.", 0.0
    entropy = estimate_entropy(password)
    if entropy < 50.0:
        return False, f"Estimated entropy {entropy:.2f} bits is too low.", entropy
    return True, "Password accepted by policy.", entropy

# ----------------------------------------------------------------------
# Lockout handling
# ----------------------------------------------------------------------
def is_locked(user_rec: Dict[str, Any]) -> tuple[bool, int]:
    """
    Returns (locked?, seconds_remaining). Refreshes lockout if expired.
    """
    locked_until_iso = user_rec.get("locked_until")
    if not locked_until_iso:
        return False, 0
    locked_until = parse_iso(locked_until_iso)
    if locked_until is None:
        return False, 0
    now = now_utc()
    if now >= locked_until:
        user_rec["locked_until"] = None
        user_rec["failed_attempts"] = 0
        return False, 0
    remaining = int((locked_until - now).total_seconds())
    return True, max(remaining, 0)

# ----------------------------------------------------------------------
# Audit log helpers
# ----------------------------------------------------------------------
def append_log(username: str, event: str, details: str = "") -> None:
    if LOG_FILE.exists():
        with LOG_FILE.open("r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = []
    log.append({
        "time": now_iso(),
        "username": username,
        "event": event,
        "details": details,
    })
    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

def load_log() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------------------------------------------------
# Registration
# ----------------------------------------------------------------------
def register_user(users: Dict[str, Any]) -> None:
    username = input("Choose a username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if username in users:
        print("That username already exists.")
        return
    password1 = getpass("Choose a password: ")
    password2 = getpass("Confirm password: ")
    if password1 != password2:
        print("Passwords do not match.")
        return
    ok, policy_msg, entropy = password_is_acceptable(password1)
    print(policy_msg)
    print(f"Estimated entropy: {entropy:.2f} bits")
    if not ok:
        print("Registration failed: password does not meet policy requirements.")
        return
    password_hash = ph.hash(password1)
    users[username] = {
        "password_hash": password_hash,
        "created_at": now_iso(),
        "last_login": None,
        "failed_attempts": 0,
        "locked_until": None,
    }
    save_users(users)
    append_log(username, "REGISTER", "New account created.")
    print("Account created successfully.")

# ----------------------------------------------------------------------
# Login
# ----------------------------------------------------------------------
def login_user(users: Dict[str, Any]) -> None:
    username = input("Username: ").strip()
    if username not in users:
        print("Unknown user.")
        return
    user = users[username]
    locked, remaining = is_locked(user)
    if locked:
        print(f"Account is currently locked. Try again in approximately {remaining} seconds.")
        return
    password = getpass("Password: ")
    try:
        ph.verify(user["password_hash"], password)
    except argon2_exceptions.VerifyMismatchError:
        # Incorrect password
        user["failed_attempts"] = int(user.get("failed_attempts", 0)) + 1
        attempts = user["failed_attempts"]
        append_log(username, "LOGIN_FAIL", f"Failed attempts: {attempts}")
        if attempts >= LOCKOUT_THRESHOLD:
            lock_until = now_utc() + timedelta(seconds=LOCKOUT_SECONDS)
            user["locked_until"] = lock_until.strftime("%Y-%m-%dT%H:%M:%SZ")
            append_log(username, "ACCOUNT_LOCKED", f"Lockout for {LOCKOUT_SECONDS} seconds.")
            print("The system has locked this account after repeated failed login attempts.")
        else:
            print("Incorrect password.")
        save_users(users)
        return
    except argon2_exceptions.VerificationError as e:
        print(f"Verification error: {e}")
        return
    # Successful login
    user["failed_attempts"] = 0
    user["locked_until"] = None
    user["last_login"] = now_iso()
    append_log(username, "LOGIN_SUCCESS", "User authenticated successfully.")
    save_users(users)
    print("Login successful. Access has been granted.")

# ----------------------------------------------------------------------
# Audit log viewing
# ----------------------------------------------------------------------
def view_audit_log() -> None:
    log = load_log()
    if not log:
        print("No audit events recorded yet.")
        return
    print("\nRecent audit events (most recent last):")
    for entry in log[-50:]:
        print(
            f"{entry['time']} | user={entry['username']} | "
            f"{entry['event']} | {entry.get('details', '')}"
        )
    print("End of audit log.\n")

# ----------------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------------
def main() -> None:
    print("Secure Authentication System (Mini Project)")
    users = load_users()
    while True:
        print("\nMenu:")
        print("  1) Register new user")
        print("  2) Login")
        print("  3) View audit log")
        print("  0) Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            register_user(users)
        elif choice == "2":
            login_user(users)
        elif choice == "3":
            view_audit_log()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Unrecognised option.")

if __name__ == "__main__":
    main()
