# Copilot Instructions for NSSec_Week05 Web Scanning Project

## Project Purpose
This is a Python utility for automated web vulnerability scanning using Wapiti, a security testing framework. The script is designed for educational security analysis on legal targets like Google Gruyere.

## Architecture Overview
**Single-file design** with modular functions:
- **`run_wapiti_scan()`** - Subprocess wrapper that executes Wapiti CLI with target URL and output directory
- **`find_latest_report()`** - Scans output directory for generated HTML reports, returns most recent by modification time
- **`open_report_in_browser()`** - Opens HTML reports using the system's default browser
- **`main()`** - Orchestrates the workflow: scan → locate report → prompt user to view

## Critical Patterns & Conventions

### Target URL Configuration
- `TARGET_URL` at top of file is the entry point (currently points to Google Gruyere educational target)
- **Always respect the legal/ethical notice**: Project is restricted to authorized training targets only
- When assisting with URL modifications, ensure users understand they should only target systems they own or have explicit permission to test

### Error Handling Approach
Three distinct error cases are explicitly caught:
1. **Missing tool** (`FileNotFoundError`) - Wapiti not installed or not in PATH; guides user to install with pip
2. **Execution failure** (`CalledProcessError`) - Wapiti ran but exited with error; reports returncode
3. **Missing report** (logic check) - Scan completed but no HTML output found; suggests troubleshooting

Do not suppress these; maintain user-friendly error messaging with `[-]` prefix for failures and `[+]` for progress.

### Report Discovery Logic
- Uses `glob.glob()` to find `*.html` files in the output directory
- Sorts by `os.path.getmtime()` in reverse order (newest first)
- Returns `Path | None` to handle missing directories/reports gracefully
- This pattern should be preserved if refactoring file handling

### Browser Integration
- Uses `webbrowser.open()` with `.as_uri()` to construct proper file:// URLs
- This is cross-platform compatible (works on macOS, Windows, Linux)
- Do not replace with direct file operations; `webbrowser` is the standard approach

## Dependencies
- **Required**: `wapiti3` (installed via pip, used as subprocess)
- **Standard Library**: subprocess, os, glob, pathlib, webbrowser
- **Python Version**: 3.10+ (uses `Path | None` union type syntax)

## Common Development Tasks

### Testing the Scan Workflow
```bash
# Install Wapiti if needed
pip install wapiti3

# Run the script against the default target
python web_scan.py
```

### Modifying the Target
Edit the `TARGET_URL` variable at the top of the file. Ensure the URL is accessible and you have explicit permission to test it.

### Debugging Wapiti Output
Output directory is stored in `OUT_DIR` variable. Check:
- `gruyere_wapiti_report/` folder for generated files
- Wapiti stdout/stderr for scan errors
- Browser console for report rendering issues

## Key Extension Points
- **New scanning engines**: Create similar `run_<scanner>_scan()` functions following the same subprocess pattern
- **Report processing**: Add post-scan analysis functions before `open_report_in_browser()`
- **UI improvements**: Replace raw `input()` prompt with better UX (e.g., argparse, conditional opening)
