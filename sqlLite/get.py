import sqlite3
from . import db_name

def get_all_users():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('select * from T_USERS')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def get_userinfo_by_username(username):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('select * from T_USERS where username = ?', (username,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def get_password_by_username(username):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT PASSWORD FROM T_USERS WHERE username = ?', (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return None
    return row[0]  # password string

def get_password_by_email(email):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT PASSWORD FROM T_USERS WHERE EMAIL = ?', (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return None
    return row[0]  # password string