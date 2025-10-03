import logging
from typing import Optional, Dict, Any
from database.interface import DatabaseInterface
from utils.password_utils import PasswordUtils
from utils.validation import ValidationUtils

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, database: DatabaseInterface):
        self.db = database

    def create_user(self, username: str, email: str, password: str) -> tuple[bool, list[str]]:
        errors = []

        # Validierung
        if not ValidationUtils.validate_username(username):
            errors.append("Invalid username format")

        if not ValidationUtils.validate_email(email):
            errors.append("Invalid email format")

        password_valid, password_errors = ValidationUtils.validate_password(password)
        if not password_valid:
            errors.extend(password_errors)

        if errors:
            return False, errors

        # Prüfe auf existierende User
        if self.get_user_by_email(email):
            errors.append("Email already registered")

        if self.get_user_by_username(username):
            errors.append("Username already taken")

        if errors:
            return False, errors

        # Passwort hashen
        password_hash = PasswordUtils.hash_password_simple(password)

        # User erstellen
        try:
            success = self.db.create_user(username, email.lower(), password_hash)
            if success:
                logger.info(f"User created successfully: {email}")
                return True, []
            else:
                logger.warning(f"Failed to create user: {email}")
                return False, ["Failed to create user"]
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False, [f"Database error: {str(e)}"]


    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if not ValidationUtils.validate_email(email):
            return None
        try:
            return self.db.get_user_by_email(email.lower())
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        if not ValidationUtils.validate_username(username):
            return None
        try:
            return self.db.get_user_by_username(username)
        except Exception as e:
            logger.error(f"Error getting user by username: {e}")
            return None