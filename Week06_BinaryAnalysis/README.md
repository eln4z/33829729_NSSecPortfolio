# Week 06 — Static Binary Analysis and Malware Triage

Overview

This exercise introduces safe, initial (static) analysis of Windows Portable Executable (PE) files to surface indicators of potential malicious behaviour without executing the sample. The focus is on extracting metadata, imports, hashes, strings, and applying YARA signatures for quick triage.

Prerequisites

- Python 3.8 or newer
- `pip` available in your PATH

Quick install

Install the minimal required libraries:

```bash
pip install pefile yara-python
```

Usage

Run the static triage script from the repository root:

```bash
python static_triage.py
```

What the script does

- Computes cryptographic hashes (MD5, SHA1, SHA256) for identification
- Prints PE import table entries to reveal API usage
- Extracts readable strings from the binary
- Attempts YARA rule matches if rules are present

Typical output (summary)

- Hashes: MD5 / SHA1 / SHA256
- Imports: list of DLLs and functions (e.g., `kernel32.dll` / `CreateProcess`) 
- Strings: notable ASCII/UTF-16 strings found in the binary
- YARA matches: matched rule names and rule metadata

Limitations

| Limitation | Explanation |
|---|---|
| No runtime visibility | Static analysis cannot observe behaviour that only appears at runtime (network calls, dropped files, registry changes). |
| Obfuscation / packing | Packed or encrypted binaries may hide imports and strings, reducing static effectiveness. |
| Signature dependency | YARA rules and signature lists only detect known patterns; novel (zero-day) samples may not match. |

Next steps / recommended workflow

- Use static triage as the first step in a layered analysis process.
- If static output is suspicious, move to controlled dynamic analysis (sandbox or VM) to observe behaviour.
- Maintain and update YARA rulesets and hash databases for better coverage.

References

- Sikorski, M., & Honig, A. (2012). Practical Malware Analysis: The Hands-On Guide to Dissecting Malicious Software.

Troubleshooting

- If `pefile` import fails, ensure you're using a compatible Python version and reinstall the package.
- For missing YARA matches, confirm rule files are available and readable by the script.

If you'd like, I can also:

- Add a `requirements.txt` with the required packages
- Add example YARA rules and a sample binary for demonstration
- Update `static_triage.py` to print sample output or create a short test harness
