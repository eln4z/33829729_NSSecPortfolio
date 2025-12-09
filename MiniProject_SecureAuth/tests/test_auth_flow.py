import builtins
import time
import sys
from pathlib import Path

# Ensure project root is on sys.path so we can import the app when running from tests/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import secure_auth_app as app

# Use a separate test DB so we don't clobber real data
TEST_DB = Path("test_auth_data.json")
if TEST_DB.exists():
    TEST_DB.unlink()
app.DATA_FILE = TEST_DB

# Keep references to originals so we can restore them
_original_input = builtins.input
_original_getpass = app.getpass


def set_inputs(values):
    it = iter(values)
    builtins.input = lambda prompt="": next(it)


def set_getpass(values):
    it = iter(values)
    app.getpass = lambda prompt="": next(it)


def restore_io():
    builtins.input = _original_input
    app.getpass = _original_getpass


def run_tests():
    db = app.load_db()

    username = "testuser"
    good_password = "Str0ng!Passphrase123"

    # 1) Register a new strong user
    set_inputs([username])
    set_getpass([good_password, good_password])
    app.register_user(db)

    assert username in db["users"], "User was not created"

    # 2) Successful login
    set_inputs([username])
    set_getpass([good_password])
    app.login_user(db)

    user = db["users"][username]
    assert user.get("failed_attempts", 0) == 0, "failed_attempts should be reset after success"
    assert any(e["event"] == "LOGIN_SUCCESS" for e in db["audit_log"]), "LOGIN_SUCCESS not logged"

    # 3) Trigger lockout by providing wrong password repeatedly
    for i in range(app.LOCKOUT_THRESHOLD):
        set_inputs([username])
        set_getpass(["wrong-password"])
        app.login_user(db)

    user = db["users"][username]
    locked = bool(user.get("locked_until"))
    assert locked, "User should be locked after threshold failures"
    assert any(e["event"] == "ACCOUNT_LOCKED" for e in db["audit_log"]), "ACCOUNT_LOCKED not logged"

    print("All tests passed.")


if __name__ == "__main__":
    try:
        run_tests()
    finally:
        # Restore I/O functions and clean up test DB
        restore_io()
        if TEST_DB.exists():
            try:
                TEST_DB.unlink()
            except Exception:
                pass
