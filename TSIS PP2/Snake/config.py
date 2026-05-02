import os
import getpass


def load_config():
    """Load DB config from environment with sensible fallbacks.

    Environment variables (optional): DB_NAME, DB_USER, DB_PASSWORD,
    DB_HOST, DB_PORT. When unset, defaults use the current OS username
    for both user and database name, and localhost:5432 for the server.
    """
    user = os.environ.get("DB_USER") or getpass.getuser()
    dbname = os.environ.get("DB_NAME") or user
    return {
        "dbname": dbname,
        "user": user,
        "password": os.environ.get("DB_PASSWORD", ""),
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "5432"),
    }