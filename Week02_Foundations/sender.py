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

# Message to send
message = b"Hello from the secure sender! This is confidential."

# Generate random AES key and IV
aes_key = os.urandom(32)
iv = os.urandom(16)

#  Encrypt message
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(message) + encryptor.finalize()

# Encrypt AES key with RSA
encrypted_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# Package as JSON
package = json.dumps({
    "encrypted_key": base64.b64encode(encrypted_key).decode("utf-8"),
    "iv": base64.b64encode(iv).decode("utf-8"),
    "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
})

# Send via socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(package.encode("utf-8"))

print("Encrypted message sent!")
