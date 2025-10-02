import sqlite3
from . import db_name

def get_user():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('select * from T_USERS')
    rows = cursor.fetchall()
    for row in rows:
        print(row)