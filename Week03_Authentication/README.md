# Week 03 — Authentication, Password Security and Access Control

## Learning Objective

This week focused on secure user authentication, including password strength measurement, secure storage through hashing and salting, and the introduction of multi-factor authentication. The aim was to critically evaluate how authentication systems defend against common attack methods, both offline and online.

## Conceptual Background

### Password Strength and Entropy

Password security relies not simply on length but on unpredictability, often expressed as entropy (Shannon, 1948). Predictable structures such as repeated characters, dictionary words or sequential numbers dramatically reduce entropy, making passwords susceptible to guessing and dictionary attacks.

### Salting and Hashing

Storing passwords in plaintext allows immediate credential compromise during a data breach. Hashing converts passwords into irreversible values, and salting ensures that identical passwords do not produce identical hashes, undermining the effectiveness of rainbow tables and large-scale cracking (Bonneau, 2012). Slow hashing functions such as Argon2 intentionally require additional processing time, making offline brute-force attacks expensive (Folly, 2020).

### Multi-Factor Authentication

Two-factor authentication adds a second requirement beyond knowledge of a password, reducing the impact of compromised credentials (Reese, 2021). Even if a password is obtained through phishing or keylogging, the attacker must still gain access to the secondary factor.

## Practical Implementation

### Password Strength Evaluation

The implementation examined password length, character diversity and common password patterns, rejecting weak choices. The system assessed effective strength through these features rather than relying solely on minimum length.

### Secure Authentication Workflow

- Passwords were hashed with Argon2 via the `argon2-cffi` library
- Individual salts were generated per user
- A lockout threshold was introduced after repeated failed attempts
- An optional two-factor step was implemented for higher assurance

## Threat Model and Evaluation

| Threat | Mitigation |
|--------|-----------|
| Offline brute-force cracking | Slow hashing using Argon2 |
| Rainbow table attacks | Salting prevents reuse of precomputed hashes |
| Credential stuffing | Password strength enforcement |
| Online guessing | Account lockout |
| Phishing or keylogging | Additional 2FA layer |

### Limitations

| Limitation | Explanation |
|-----------|------------|
| Local file-based storage | No secure database controls |
| No encryption at rest | Relies solely on hashing for protection |
| 2FA dependent on shared secret | Device compromise undermines second factor |

Large-scale systems use encrypted credential databases, hardware security modules and identity federation protocols such as OAuth and WebAuthn to strengthen assurance (FIDO Alliance, 2020).

## Reflection

This activity demonstrated that passwords remain viable when appropriately managed, rather than inherently insecure. The critical vulnerabilities arise from poor storage practices and inadequate defensive layers rather than user-generated secrets alone. Implementing Argon2 hashing, salting and two-factor authentication highlighted the importance of layered controls that address both offline and online threats. The exercise reinforced that authentication security is not a single mechanism but a coordinated set of countermeasures responding to specific threat models.

## Usage

Run the main program:

```bash
python main.py
```
