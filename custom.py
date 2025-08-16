# custom.py
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Put database file under ./db by default
DEFAULT_DB = ROOT / "db" / "gitgrub.sqlite3"
DB_PATH = os.getenv("DB_PATH", str(DEFAULT_DB))

# Flask secret key (do NOT hard-code)
SECRET_KEY = os.getenv("SECRET_KEY", None)

# Optional admin bootstrap (used by seed.py)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", None)  # if None, seed will generate

