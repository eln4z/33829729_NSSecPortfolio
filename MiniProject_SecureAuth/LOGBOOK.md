# Mini-Project Logbook — Secure Authentication CLI

Project title

Secure Authentication CLI with Argon2 lockout and audit logging

Duration

Week 08 onward (Mini-Project)

---

1) Planning

Aim

Design and implement a secure login system that mitigates weak passwords, credential guessing, and brute-force attacks using techniques covered in the NSSec module.

Security problem

Many simple login systems use fast hashing (e.g., MD5 or SHA-1), lack a password policy, and allow unlimited login attempts. These issues enable attackers to crack leaked hashes or perform online guessing.

Rationale

A compact, well-designed authentication component can materially improve security for small applications and prototypes.

Planned features

| Feature                    | Justification                          |
| -------------------------- | -------------------------------------- |
| Password scoring + entropy | Discourages predictable credentials    |
| Argon2id hashing           | Memory-hard, resistant to GPU cracking |
| Account lockout            | Prevents online guessing attempts      |
| Audit logging              | Enables post-incident analysis         |
| JSON storage               | Lightweight and easy to inspect        |

Project breakdown

| Task                            | Deliverable             |
| ------------------------------- | ----------------------- |
| Research weak password risks    | Requirements + design   |
| Build Argon2-based registration | Hash storage            |
| Implement lockout + timing      | Intrusion throttling    |
| Add audit logging               | Forensics + observation |
| Test + document scenarios       | Evidence + reflection   |

---

2) Implementation

Tools & libraries

- Python 3
- `argon2-cffi` for Argon2id hashing
- Standard libraries: `json`, `datetime`, `getpass`, etc.

System overview

| Component             | Description                                 |
| --------------------- | ------------------------------------------- |
| `password_strength()` | Scores password and estimates entropy       |
| `register_user()`     | Rejects weak passwords and stores Argon2 hash |
| `login_user()`        | Verifies hash and updates failure counters  |
| `is_locked()`         | Applies lockout after threshold failures    |
| `log_event()`         | Records security events to an audit log     |
| `view_audit_log()`    | Shows recent authentication events          |

Data storage (example)

```json
{
  "users": {
    "alice": {
      "password_hash": "$argon2id$v=19$...",
      "failed_attempts": 0,
      "locked_until": null
    }
  },
  "audit_log": [
    { "time": "...", "username": "alice", "event": "REGISTER" }
  ]
}
```

---

3) Testing

Test environment

- Local Python environment (no network access)
- Tests use a temporary JSON file so local data is not overwritten

Test cases & results (summary)

| ID | Action                                | Expected outcome                      | Result |
|----|---------------------------------------|---------------------------------------|--------|
| T1 | Register with weak password           | Rejected, no user created             | Pass   |
| T2 | Register with a strong password       | User created, hash stored             | Pass   |
| T3 | Five incorrect logins                 | Account locked and logged             | Pass   |
| T4 | Login while locked                    | Blocked until unlock time             | Pass   |
| T5 | Correct login after unlock            | Success, counters reset               | Pass   |
| T6 | View audit log                        | Shows register/fail/lock/success      | Pass   |

Evidence to include

- Example registration output
- Failed login attempts leading to lockout
- JSON file showing hashed password entries
- Audit log snippet with timestamps and events

---

4) Evaluation and reflection

This project shows that meaningful security improvements can be achieved with modest changes: using Argon2id for password hashing, enforcing sensible password policies, applying lockout thresholds, and keeping an audit trail. Logging failed attempts provides forensic value and helps tune detection thresholds.

Limitations

The current design is intentionally lightweight. JSON storage lacks encryption, access controls, and proper concurrency handling. For production use, replace JSON with a secure database, add transport security (TLS), and consider multi-factor authentication.

---

5) Future improvements

| Enhancement           | Benefit                               |
| --------------------- | ------------------------------------- |
| Add MFA (e.g., TOTP)  | Reduces impact of password theft      |
| Encrypt user DB       | Protects data at rest                 |
| Use SQLite/PostgreSQL | Improves scalability and integrity    |
| Add API + web UI      | Move toward a production prototype    |
| Export logs for SIEM  | Enterprise monitoring integration     |
