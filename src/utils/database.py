import sqlite3


def connect_to_db(dbname: str):
    conn = sqlite3.connect(dbname)
    return conn.cursor()
