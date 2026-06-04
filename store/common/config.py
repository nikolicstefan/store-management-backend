import os


class Config:
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "user")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "pass")
    DATABASE_URL      = os.environ.get("DATABASE_URL", "localhost")
    DATABASE_NAME     = os.environ.get("DATABASE_NAME", "store")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL}/{DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "JWT_SECRET_DEV_KEY")
