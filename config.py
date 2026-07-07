import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "autorescue-dev-secret")

    DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
    DB_ENGINE = os.environ.get("DB_ENGINE", "sqlite").strip().lower()
    SQLITE_DB_NAME = os.environ.get("SQLITE_DB_NAME", "autorescue.db").strip() or "autorescue.db"

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "autorescue_v2")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif DB_ENGINE == "mysql":
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        sqlite_path = (BASE_DIR / SQLITE_DB_NAME).resolve()
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path.as_posix()}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"check_same_thread": False},
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": 10,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
        }
