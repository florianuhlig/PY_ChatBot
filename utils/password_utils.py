import hashlib
import logging
import secrets

logger = logging.getLogger(__name__)


class PasswordUtils:
    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple[str, str]:
        if salt is None:
            salt = secrets.token_hex(32)
        password = password.strip()
        salted_password = password + salt
        hash_object = hashlib.sha512(salted_password.encode("utf-8"))
        password_hash = hash_object.hexdigest()
        logger.debug("Password hashed successfully")
        return password_hash, salt

    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str) -> bool:
        computed_hash, _ = PasswordUtils.hash_password(password, salt)
        return secrets.compare_digest(computed_hash, stored_hash)

    @staticmethod
    def hash_password_simple(password: str) -> str:
        password = password.strip()
        return hashlib.sha512(password.encode("utf-8")).hexdigest()
