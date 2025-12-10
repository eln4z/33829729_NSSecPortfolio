from pathlib import Path
import sys
sys.path.insert(0, '.')
import secure_auth_app as app, builtins

username = 'demo_user'
pwd = 'DemoPass!2345'

# Mock interactive prompts
builtins.input = lambda prompt='': username
app.getpass = lambda prompt='': pwd

# Register the user
db = app.load_db()
if username in db.get('users', {}):
    print('User already exists in DB:', username)
else:
    app.register_user(db)
    print('Registered user:', username)

print('Data file path:', app.DATA_FILE.resolve())
