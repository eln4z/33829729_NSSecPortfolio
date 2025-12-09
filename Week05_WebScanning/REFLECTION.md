# Week 05: Web Vulnerability Scanning - Reflection & Portfolio

## 🎯 Reflection

Using Wapiti helped me understand how automated scanners perform black-box testing, meaning the tool does not need access to source code and instead crawls a web application to discover and probe its inputs. This directly supports the seminar objective of identifying security weaknesses through automated requests and response analysis.

The scan of Google Gruyere revealed vulnerabilities such as XSS and insecure file upload, which occur because user input is not validated before being executed or stored. These weaknesses highlight how simple coding mistakes can lead to serious exploitation.

However, scanners like Wapiti can miss business-logic vulnerabilities or produce false positives, showing that automated tools alone are insufficient. Combining automated scanning with manual review, secure coding practices, and regular auditing aligns with the workshop's emphasis on preventing attacks before exploitation.

---

## 📸 Screenshots Required

Place the following screenshots in the `screenshots/` folder:

| Screenshot | Purpose |
|-----------|---------|
| `1_web_scan_py_code.png` | VS Code showing `web_scan.py` script |
| `2_terminal_scanning.png` | Terminal output during Wapiti execution |
| `3_report_folder.png` | `gruyere_wapiti_report/` folder with HTML output |
| `4_browser_report.png` | HTML vulnerability report open in browser |

---

## ✅ Week 05 Completion Checklist

- [x] Ethical disclaimer included (in `web_scan.py`)
- [x] Used authorized target (Google Gruyere)
- [x] Installed and ran Wapiti
- [x] Created VS Code Python script (`web_scan.py`)
- [ ] **TODO:** Add 4 screenshots to `screenshots/` folder
- [ ] **TODO:** Review reflection text above

Once screenshots are added, Week 05 is complete!
