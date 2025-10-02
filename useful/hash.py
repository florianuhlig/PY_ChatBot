from hashlib import sha512

def get_password_hash(password):
    password = password.strip()
    return sha512(password.encode('utf-8')).hexdigest()