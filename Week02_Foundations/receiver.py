# receiver.py (safe JSON + Base64)
import socket, json, base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HOST = "127.0.0.1"
PORT = 65432

# Load private key
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Waiting for connection on {HOST}:{PORT} ...")

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # Read till the client closes the connection
        chunks = []
        while True:
            chunk = conn.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
        raw = b"".join(chunks).decode("utf-8")

        if not raw:
            print("No data received.")
        else:
            package = json.loads(raw)
            enc_key = base64.b64decode(package["encrypted_key"])
            iv = base64.b64decode(package["iv"])
            ciphertext = base64.b64decode(package["ciphertext"])

            # RSA decrypt AES key
            aes_key = private_key.decrypt(
                enc_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

            # AES decrypt message
            cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
            decryptor = cipher.decryptor()
            message = decryptor.update(ciphertext) + decryptor.finalize()

            print("Decrypted message:", message.decode("utf-8"))
