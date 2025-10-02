import re

def check_email(email):
    # Click on Edit and place your email ID to validate
    #email = "my.ownsite@our-earth.de"
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if valid:
        return True
    else:
        return False