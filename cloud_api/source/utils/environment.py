import os


def env_database():
    database = {
        "POSTGRES_DATABASE": os.getenv("POSTGRES_DATABASE", "default_db"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT", "5432"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER", "postgres"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD", "")
    }

    return database
