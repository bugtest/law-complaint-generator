import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 数据库
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/law_system.db")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-me")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# 文件存储
FILE_STORAGE_PATH = Path(os.getenv("FILE_STORAGE_PATH", BASE_DIR / "docs" / "storage"))
FILE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))

# AI
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "qwen3.5-plus")

# OCR
OCR_ENABLED = os.getenv("OCR_ENABLED", "true").lower() == "true"
OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "ch")

# 日志
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = Path(os.getenv("LOG_FILE", BASE_DIR / "logs" / "app.log"))
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
