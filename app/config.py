from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "chat.db"
SECRET_KEY = "mysq8vB9_kF1n4xTtPjvLz2H6aR5mE7wY0pecretkey"  # for JWT
