import sqlite3
from . import db_name

## Create Tables
def create_table_t_user():
    db_con = sqlite3.connect(db_name)
    db_cur = db_con.cursor()
    db_cur.execute("""
    CREATE TABLE IF NOT EXISTS T_USERS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        USERNAME TEXT NOT NULL UNIQUE,
        EMAIL TEXT NOT NULL UNIQUE,
        PASSWORD TEXT NOT NULL
    );""")
    db_con.commit()