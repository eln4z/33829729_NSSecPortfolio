# sender.py (safe JSON + Base64)
import socket, os, json, base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HOST = "127.0.0.1"
PORT = 65432

# Load recipient's public key
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Message to send (change this or prompt for input)
message = b"Hello from the secure sender! This is confidential."

# 1) Generate random AES key and IV
aes_key = os.urandom(32)  # AES-256
iv = os.urandom(16)

# 2) Encrypt message with AES (CFB mode)
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(message) + encryptor.finalize()

# 3) Encrypt AES key with RSA (recipient's public key)
encrypted_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# 4) Package as JSON (Base64-encoded fields)
package = json.dumps({
    "encrypted_key": base64.b64encode(encrypted_key).decode("utf-8"),
    "iv": base64.b64encode(iv).decode("utf-8"),
    "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
})

# 5) Send via socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(package.encode("utf-8"))

print("✅ Encrypted message sent!")
