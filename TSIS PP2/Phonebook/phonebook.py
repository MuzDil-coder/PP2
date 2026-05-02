import sqlite3
import os

def connect():
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, "phonebook.db")

    conn = sqlite3.connect(db_path)
    return conn