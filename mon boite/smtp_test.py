import os
from pathlib import Path
import smtplib


def load_env_file():
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        os.environ.setdefault(key, value)


load_env_file()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_TO = os.getenv("SMTP_TO", "mahsumim588@gmail.com")

if not SMTP_USER or not SMTP_PASSWORD:
    print("Missing SMTP_USER or SMTP_PASSWORD in .env")
    raise SystemExit(1)

try:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    print("SMTP connection successful.")
    server.sendmail(SMTP_USER, SMTP_TO, "Subject: Test Maison Impeccable\n\nSMTP test OK")
    print(f"Test email sent to {SMTP_TO}")
    server.quit()
except Exception as exc:
    print(f"SMTP test failed: {exc}")
    raise SystemExit(1)
