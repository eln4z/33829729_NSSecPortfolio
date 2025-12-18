# Network and System Security (2025–26) — Coursework Portfolio

This repository contains practical coursework for the *Network and System Security (2025–26)* module. It includes weekly security exercises and a final mini-project demonstrating applied techniques in secure system design and analysis.

## Weekly Summary

| Week | Topic | Summary |
|------|-------|---------|
| 01 | Security Foundations & Python Setup | Introduced the CIA triad and completed an introductory Python notebook to prepare for later security tooling. |

| 02 | Secure Communication | Implemented a hybrid RSA–AES encrypted messaging demonstration. |

| 03 | Authentication Security | Applied entropy-based password policy, Argon2id hashing and account lockout. |

| 04 | File Integrity Monitoring | Built baseline hashing and change detection to identify file tampering. |

| 05 | Web Vulnerability Scanning | Performed ethical scanning of an approved target and analysed results. |

| 06 | Static Binary Analysis | Conducted basic malware triage using hashing and static inspection. |

| 07 | Network Reconnaissance | Applied authorised reconnaissance and service enumeration techniques. |

| 08 | Portfolio Development | Structured documentation, evidence and reflections for assessment. |

| 09 | AI Security Testing | Tested prompt manipulation and output behaviour in generative AI systems. |

## Mini-Project — Secure Authentication System

A local authentication system featuring:
- Balanced, entropy-based password policy
- Argon2id password hashing
- Account lockout after repeated failures
- Optional two-factor authentication
- JSON-based audit logging

### How to Run
```bash
pip install argon2-cffi
python secure_auth_app.py
