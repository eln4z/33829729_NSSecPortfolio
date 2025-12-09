import subprocess
import os
import glob
import webbrowser
from pathlib import Path

# ⚠️ Only use LEGAL training targets like Google Gruyere, as in the workshop. :contentReference[oaicite:0]{index=0}
TARGET_URL = "https://google-gruyere.appspot.com/123456/"   # replace with *your* instance URL if you have one
OUT_DIR = "gruyere_wapiti_report"                    # folder for Wapiti output


def run_wapiti_scan(target: str, out_dir: str):
    """
    Run Wapiti as a subprocess against the given target URL.
    Equivalent to:
        wapiti -u <target> -o <out_dir>
    """
    print(f"[+] Starting Wapiti scan on: {target}")
    cmd = ["wapiti", "-u", target, "-o", out_dir]

    # Run Wapiti and stream output to the terminal
    try:
        subprocess.run(cmd, check=True)
        print("[+] Scan finished.")
    except FileNotFoundError:
        print("[-] Error: 'wapiti' command not found.")
        print("    Make sure you installed it with: pip install wapiti3")
        print("    And that your PATH / virtualenv is set correctly.")
    except subprocess.CalledProcessError as e:
        print("[-] Wapiti exited with an error code:", e.returncode)


def find_latest_report(out_dir: str) -> Path | None:
    """
    Find the most recent HTML report inside the output directory.
    """
    out_path = Path(out_dir)
    if not out_path.exists():
        return None

    # Look for any .html files inside the directory
    matches = glob.glob(str(out_path / "*.html"))
    if not matches:
        return None

    matches.sort(key=os.path.getmtime, reverse=True)
    return Path(matches[0])


def open_report_in_browser(report_path: Path):
    """
    Open the Wapiti HTML report in the default web browser.
    """
    print(f"[+] Opening report in browser: {report_path}")
    webbrowser.open(report_path.as_uri())


def main():
    # 1) Run the scan
    run_wapiti_scan(TARGET_URL, OUT_DIR)

    # 2) Locate latest report
    report = find_latest_report(OUT_DIR)
    if report is None:
        print("[-] No HTML report found. Check Wapiti output.")
        return

    print(f"[+] Report generated at: {report.resolve()}")

    # 3) Ask user if they want to open it
    ans = input("Open report in browser? [y/N]: ").strip().lower()
    if ans == "y":
        open_report_in_browser(report)


if __name__ == "__main__":
    main()
