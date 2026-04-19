from datetime import timedelta
import os


class Config:
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "user")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "pass")
    DATABASE_URL      = os.environ.get("DATABASE_URL", "localhost")
    DATABASE_NAME     = os.environ.get("DATABASE_NAME", "auth")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL}/{DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
