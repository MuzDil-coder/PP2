import psycopg2
import sys
from config import load_config


def connect():
    config = load_config()

    try:
        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL")
        return conn

    except Exception as error:
        print("Database connection failed:", error)
        sys.exit(1)


if __name__ == "__main__":
    connect()