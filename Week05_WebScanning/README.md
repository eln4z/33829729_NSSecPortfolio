**Week 05 — Web Vulnerability Scanning**

**Overview:** This repository contains a small Python wrapper (`web_scan.py`) that automates running the Wapiti web scanner against a target URL and saving an HTML report in `gruyere_wapiti_report/`. The exercise focuses on learning automated discovery techniques while respecting legal and ethical boundaries.

**Learning Objective:** Understand capabilities and limitations of automated web scanners and practise ethical reconnaissance on authorised targets only.

**Background:**
- **Tools used:** Wapiti (CLI) via the `wapiti3` package.
- **Common checks:** SQL injection, cross-site scripting (XSS), local file inclusion (LFI), and other input-based issues.
- **Limitations:** Automated scanners reveal potential issues but do not prove exploitability or business-impact — manual verification is required.

**Prerequisites:**
- **Python:** 3.10+ (the code uses modern typing and standard library modules).
- **Wapiti:** Install with `pip install wapiti3` or follow project docs if you prefer a system package.

**Quick Start:**
- Install dependency:

```
pip install wapiti3
```

- Run the scanner wrapper:

```
python web_scan.py
```

- The script will prompt for a target URL. Example approved training targets: `http://<your-dvwa-host>/`, `http://<juice-shop-host>/`, or the Google Gruyere lab used in class.

**Where reports are saved:**
- Output HTML reports are placed in the `gruyere_wapiti_report/` directory. Example files in this repo: `report.html` and `google-gruyere.appspot.com_12092025_1640.html`.
- To open a report manually, run:

```
open gruyere_wapiti_report/report.html
```

**Ethics & Legal Notice:**
- Only scan systems you own or have explicit written permission to test. Unauthorized scanning can be illegal and harmful.
- Prefer isolated labs and intentionally vulnerable targets for learning (DVWA, Juice Shop, Gruyere).
- If you discover sensitive data or real vulnerabilities on authorised targets, follow a responsible disclosure process.

**Practical Notes & Limitations:**
- Scanners produce false positives; treat results as leads, not confirmed issues.
- Automated checks cannot detect business-logic flaws or guarantee exploitability.
- Scans can be noisy and may trigger alerts or cause service disruption — use low-impact settings on shared targets.

**Files of interest:**
- `web_scan.py`: Python wrapper that runs Wapiti and locates the latest HTML report.
- `gruyere_wapiti_report/`: Directory with generated HTML reports and assets.
- `screenshots/`: Example output screenshots from the lab exercises (if present).

**Next steps (suggested):**
- Try running the wrapper against a lab instance and open the generated report.
- Extend the wrapper to accept command-line args (e.g., `--outdir`, `--profile`) or add a results parser.

**References & Further Reading:**
- Wapiti project: https://wapiti.sourceforge.io/
- OWASP testing guide: https://owasp.org/

**Author / Course:** Week 05 — Networking / Web Scanning lab

---
_This README is intended for educational purposes and assumes all scans are performed against authorised, legal test targets._