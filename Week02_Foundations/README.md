Week 02 — Secure Network Foundations (Hybrid Cryptography)
Learning Objective

This week focused on applying public-key and symmetric cryptography to secure network communication. The objective was to develop an understanding of how confidentiality is achieved in data transmission and how real systems, such as TLS, combine cryptographic primitives to achieve both performance and security.


This small demo illustrates a hybrid encryption pattern: RSA is used to securely transport a randomly generated AES key, and AES encrypts the actual message payload that is sent over a local TCP socket.

Files
- `generate_keys.py` — creates `private_key.pem` and `public_key.pem` (PEM format).
- `receiver.py` — TCP server that loads `private_key.pem`, receives a JSON package, RSA-decrypts the AES key, and decrypts the message.
- `sender.py` — TCP client that generates an AES key + IV, encrypts the message with AES, RSA-encrypts the AES key using `public_key.pem`, and sends a base64-encoded JSON package.

Quick start

1. Install the dependency (tested on Python 3.8+):

```bash
pip install cryptography
```

2. Generate an RSA key pair (creates `private_key.pem` and `public_key.pem` in the current directory):

```bash
python generate_keys.py
```

3. Start the receiver in one terminal:

```bash
python receiver.py
```

4. In another terminal, run the sender to transmit an encrypted message:

```bash
python sender.py
```

You should see the decrypted message printed in the receiver terminal.

Wire format
- The sender sends a single JSON object (UTF-8 text) with three Base64-encoded fields:

```json
{
	"encrypted_key": "<base64>",
	"iv": "<base64>",
	"ciphertext": "<base64>"
}
```

Notes & conventions
- Host/port: The demo uses `127.0.0.1:65432`. Both scripts reference these constants — if you change them, update both files and this README.
- Key files: `generate_keys.py` writes `private_key.pem` (PKCS8, no password) and `public_key.pem` (SubjectPublicKeyInfo). The scripts load these filenames from the current working directory.
- Crypto details (explicit): RSA-OAEP with SHA-256; AES-256 in CFB mode (32-byte key + 16-byte IV). See `sender.py` and `receiver.py` for the exact implementations.

Security limitations (educational demo)
- No authentication or identity verification — susceptible to MITM. The receiver trusts whoever connects to the socket.
- AES-CFB is unauthenticated; messages have no integrity check. A better production choice is AES-GCM (authenticated encryption).
- Long-term use of a single RSA key is discouraged — use ephemeral key exchange (e.g., ECDHE) for forward secrecy in real systems.

Suggested small improvements
- Add an `argparse` CLI for `--host`, `--port`, and a message argument in `sender.py`.
- Migrate symmetric encryption to AES-GCM and include the authentication tag in the JSON package.
- Add unit tests or a small integration script that runs the receiver and sender automatically to validate end-to-end behavior.

If you want, I can implement one of the suggested improvements (CLI flags, AES-GCM migration, or an automated test harness). Tell me which and I'll update the code and README accordingly.
