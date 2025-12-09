import hashlib, bcrypt

def hash_demo(password: str):
    b = password.encode()
    md5_hash = hashlib.md5(b).hexdigest()
    sha256_hash = hashlib.sha256(b).hexdigest()
    bcrypt_hash = bcrypt.hashpw(b, bcrypt.gensalt()).decode()
    return md5_hash, sha256_hash, bcrypt_hash
