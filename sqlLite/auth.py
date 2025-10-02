
def login(name_email, password):
    import get as getter
    password_stored = getter.get_password_by_email(name_email)
    if password_stored is None:
        return None
    elif password_stored != password:
        return None
    else:
        return True

def register(username, email, password):
    import standard.getter as st_getter
    if st_getter.get_validate_email(email):
        hashed_password = st_getter.get_password_hash(password)
        import sqlLite.set as sq_setter
        sq_setter.set_login(username, email,hashed_password)