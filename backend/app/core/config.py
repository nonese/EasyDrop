import os
from pathlib import Path


class Settings:
    APP_NAME = "EasyDrop Ad Delivery"
    API_PREFIX = "/api"
    JWT_SECRET = os.getenv("JWT_SECRET", "change-this-in-production")
    JWT_ALG = "HS256"
    ADMIN_TOKEN_EXPIRE_MIN = int(os.getenv("ADMIN_TOKEN_EXPIRE_MIN", "60"))
    DEVICE_TOKEN_EXPIRE_MIN = int(os.getenv("DEVICE_TOKEN_EXPIRE_MIN", str(60 * 24 * 30)))

    BASE_DIR = Path(__file__).resolve().parents[3]
    DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "app.db"))
    STORAGE_DIR = Path(os.getenv("STORAGE_DIR", str(BASE_DIR / "storage")))
    MEDIA_DIR = STORAGE_DIR / "media"
    THUMB_DIR = STORAGE_DIR / "thumb"
    MANIFEST_DIR = STORAGE_DIR / "manifest"

    ADMIN_INIT_USERNAME = os.getenv("ADMIN_INIT_USERNAME", "admin")
    ADMIN_INIT_PASSWORD = os.getenv("ADMIN_INIT_PASSWORD", "admin123")

    ALLOWED_MIME = {
        "video/mp4",
        "video/webm",
        "image/jpeg",
        "image/png",
    }
    MAX_UPLOAD_SIZE_BYTES = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", str(500 * 1024 * 1024)))


settings = Settings()
