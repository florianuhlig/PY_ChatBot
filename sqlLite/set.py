from hashlib import sha512
import sqlite3
import standard.getter as st_getter
from . import db_name

def set_login(username, email, password):
    db_con = sqlite3.connect(db_name)
    db_cur = db_con.cursor()
    try:
        if st_getter.get_validate_email(email):
            db_cur.execute("INSERT INTO T_USERS (USERNAME, EMAIL, PASSWORD) VALUES (?,?,?)", (username ,email , st_getter.get_password_hash(password)))
            db_con.commit()
        else:
            print("Email entered is not valid")
    except sqlite3.IntegrityError:
        print("Username or Email entered is not unique")
    db_con.close()