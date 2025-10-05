import logging
import re

logger = logging.getLogger(__name__)


class ValidationUtils:
    @staticmethod
    def validate_email(email: str) -> bool:
        if not email or not isinstance(email, str):
            return False

        email = email.strip().lower()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        is_valid = bool(re.match(pattern, email))

        if not is_valid:
            logger.warning(f"Invalid email format: {email}")

        return is_valid

    @staticmethod
    def validate_username(username: str) -> bool:
        if not username or not isinstance(username, str):
            return False
        username = username.strip()
        # Username-Regeln: 3-25 Zeichen, nur Buchstaben, Zahlen und Unterstrich
        if len(username) < 3 or len(username) > 25:
            logger.warning(f"Username length invalid: {len(username)}")
            return False
        pattern = r"^[a-zA-Z0-9_]+$"
        is_valid = bool(re.match(pattern, username))
        if not is_valid:
            logger.warning(f"Invalid username format: {username}")
        return is_valid

    @staticmethod
    def validate_password(password: str) -> tuple[bool, list[str]]:
        errors = []
        if not password or not isinstance(password, str):
            errors.append("Password is required")
            return False, errors
        if len(password) < 4 or len(password) > 50:
            errors.append(
                "Password must be at least 4 characters long and must not exceed 128 characters"
            )
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        is_valid = len(errors) == 0
        if not is_valid:
            logger.warning(f"Password validation failed: {errors}")

        return is_valid, errors
