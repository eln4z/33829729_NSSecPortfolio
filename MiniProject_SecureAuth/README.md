# Secure Authentication — Mini Project

A small, local authentication system demonstrating practical defenses for password-based login: entropy-based password policy, memory-hard hashing (Argon2id), account lockout on repeated failures, and simple audit logging.

## Features
- Entropy-aware password acceptance (encourages long/passphrases)
- Password hashing using `argon2-cffi` (Argon2id)
- Account lockout after configurable failed attempts
- JSON-backed datastore (`auth_data.json`) and audit log
- Simple CLI interface for registering and logging in

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt` (install with pip)

## Quick Start

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app (interactive CLI):

```bash
python secure_auth_app.py
```

4. A simple registration demo is available:

```bash
python scripts/register_demo.py
```

## Files of Interest
- `secure_auth_app.py`: Main application code (register/login, password policy, hashing)
- `auth_data.json`: Stores user records (salts, hashes, lockout metadata)
- `tests/test_auth_flow.py`: Lightweight integration-style test script
- `scripts/register_demo.py`: Small script to demonstrate creating a user
- `requirements.txt`: Python package dependencies

## Running Tests
The repository includes a simple test script that exercises register/login and lockout flows. Run it directly:

```bash
python tests/test_auth_flow.py
```

The script prints `All tests passed.` on success. (It uses assertions and a temporary test DB file.)

## Security Notes
- Passwords are stored only as salted Argon2id hashes; no plaintext passwords are written to disk.
- Account lockout and audit logging support basic defensive controls against online guessing and provide an evidence trail.
- This project is intended for educational purposes; for production use, consider server-side protections, encrypted storage, and hardened deployment patterns.

## Contributing
Bug reports, improvements, and documentation fixes are welcome. Open an issue or submit a pull request describing the change.

## License
This project is provided for educational use. Include your preferred license here if you plan to publish.
Understood — you want **paraphrased output descriptions**, not quoted CLI messages.

I will now **revise the Mini-Project README** to remove all literal output text and replace it with third-person descriptions such as:

> The system locked the account after repeated failed login attempts.

Here is the updated version:

---

# Mini-Project — Secure Authentication System (Balanced Usability Security)

## Project Overview

This mini-project presents a secure local authentication system implementing layered controls to protect user credentials. The solution incorporates a password policy based on entropy rather than artificial complexity, a memory-hard hashing mechanism (Argon2id), account lockout to prevent online guessing, and audit logging to support forensic accountability. The design reflects practical defensive security, prioritising misuse prevention and operational viability rather than theoretical encryption alone.

## Security Design Principles

### Balanced Usability Policy

The solution applies an entropy-based password policy that allows long, memorable phrases rather than requiring complex character combinations. This approach aims to encourage strong user behaviour without enforcing patterns that users typically bypass or misapply (NIST, 2020). For example, a long, unpredictable phrase may be accepted even without symbols, as entropy rather than formatting determines strength.

### Argon2id Password Hashing

Argon2id was chosen due to its memory-hard design, making high-volume brute-force attacks expensive to perform on GPUs. By comparison, bcrypt uses limited memory, and PBKDF2 does not scale resistance against parallel attackers effectively (Folly, 2020). Argon2id therefore reduces the feasibility of offline cracking where an adversary has obtained the credential database.

### Layered Security Controls

Security is achieved through interdependent mechanisms:

| Mechanism                          | Purpose                                         |
| ---------------------------------- | ----------------------------------------------- |
| Entropy-based password policy      | Reduces predictable or dictionary-based choices |
| Argon2id hashing with salt         | Prevents reversible storage and hash reuse      |
| Account lockout                    | Restricts repeated guessing attempts            |
| Optional two-factor authentication | Reduces impact of credential exposure           |
| JSON audit log                     | Supports accountability and detection of misuse |

This approach highlights that no individual safeguard fully protects authentication; defence requires multiple reinforcement points.

---

## How to Run the Program

### 1. Install Dependency

```
pip install argon2-cffi
```

### 2. Launch the Authentication System

```
python secure_auth_app.py
```

### 3. Expected Behaviour (Paraphrased)

* Weak passwords are rejected, and the user is prompted to choose a stronger one.
* Accounts are created only when password entropy meets policy requirements.
* Successful authentication results in confirmed access.
* Repeated failed attempts cause the system to lock the affected account until the cooldown expires.
* A log view reveals recorded actions, including lockouts and successful access sessions, with timestamps.

### 4. Generated Files

The following files are automatically produced in the working directory:

| File             | Purpose                                                      |
| ---------------- | ------------------------------------------------------------ |
| `auth_data.json` | Stores usernames, salted Argon2id hashes, lockout metadata   |
| `audit_log.json` | Records authentication events for analysis and investigation |

No plaintext or reversible password material is stored.

---

## Limitations and Future Improvements

| Current Constraint                  | Potential Enhancement                                     |
| ----------------------------------- | --------------------------------------------------------- |
| Local file-based credential storage | Use encryption, TPM-backed secrets or database protection |
| Basic two-factor implementation     | Add app-based QR enrolment or hardware tokens             |
| CLI-based interaction               | Extend to a secure GUI or web service with HTTPS          |
| No session token management         | Add signed session tokens to manage access duration       |

The system reflects core defensive principles but does not represent a full enterprise deployment.

---

## Ethical and Legal Considerations

As authentication mechanisms handle sensitive data, responsible design requires avoidance of direct personal identifiers and secure storage of credential representations. Storing salted, irreversible hashes limits exposure even if the local system is compromised. Audit logging supports accountability if misuse occurs, aligning with secure system design guidelines and forensic expectations.

