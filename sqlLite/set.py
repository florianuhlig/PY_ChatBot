from hashlib import sha512
import sqlite3
import useful.check as check
from . import db_name

def set_password_hash(password):
    return sha512(password.encode('utf-8')).hexdigest()

def set_login(email, password):
    db_con = sqlite3.connect(db_name)
    db_cur = db_con.cursor()
    try:
        if check.check_email(email):
            db_cur.execute("INSERT INTO T_USERS (USERNAME, EMAIL, PASSWORD) VALUES (?,?,?)", ('test',email, set_password_hash(password)))
            db_con.commit()
        else:
            print("Email entered is not valid")
    except sqlite3.IntegrityError:
        print("Username or Email entered is not unique")