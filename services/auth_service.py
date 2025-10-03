import logging
from typing import Optional, Dict, Any
from database.interface import DatabaseInterface
from utils.password_utils import PasswordUtils
from utils.validation import ValidationUtils

logger = logging.getLogger(__name__)

class AuthService:

    def __init__(self, database: DatabaseInterface):
        self.db = database

    def authenticate(self, email: str, password: str) -> tuple[bool, Optional[Dict[str, Any]], str]:
        if not ValidationUtils.validate_email(email):
            return False, None, "Invalid email format"

        if not password:
            return False, None, "Password is required"
        try:
            # User holen
            user = self.db.get_user_by_email(email.lower())
            if not user:
                logger.warning(f"Authentication failed: user not found for email {email}")
                return False, None, "Invalid email or password"
            # Passwort prüfen
            stored_hash = user.get('password_hash')
            if not stored_hash:
                logger.error(f"No password hash found for user {email}")
                return False, None, "Authentication error"
            # Einfacher Hash-Vergleich (für Rückwärtskompatibilität)
            entered_hash = PasswordUtils.hash_password_simple(password)

            if entered_hash == stored_hash:
                logger.info(f"Authentication successful for user: {email}")
                # Sensible Daten nicht zurückgeben
                safe_user_data = {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'created_at': user.get('created_at')
                }
                return True, safe_user_data, "Authentication successful"
            else:
                logger.warning(f"Authentication failed: wrong password for email {email}")
                return False, None, "Invalid email or password"

        except Exception as e:
            logger.error(f"Authentication error for email {email}: {e}")
            return False, None, "Authentication error"
