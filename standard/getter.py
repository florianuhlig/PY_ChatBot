def get_password_hash(password):
    from hashlib import sha512
    password = password.strip()
    return sha512(password.encode('utf-8')).hexdigest()

def get_validate_email(email):
    import re
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if valid:
        return True
    else:
        return False