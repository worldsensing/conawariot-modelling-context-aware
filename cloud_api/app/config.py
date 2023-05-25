import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)  # default postgres port
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "apidb")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    EXTERNAL_URL = str = os.getenv("EXTERNAL_URL", "http://34.122.80.205:8000")

    cors_origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        EXTERNAL_URL
    ]


settings = Settings()
