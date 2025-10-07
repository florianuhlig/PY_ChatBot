import logging
import sqlite3
from pathlib import Path
from threading import local
from typing import Any, Dict, Optional

from .interface import DatabaseInterface

logger = logging.getLogger(__name__)


class SQLiteDatabase(DatabaseInterface):
    """Thread-Safe SQLite-Implementierung der Database-Interface"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        # Erstelle Verzeichnis falls nicht vorhanden
        self._ensure_database_directory()
        # Thread-local storage für Verbindungen
        self._local = local()

    def _ensure_database_directory(self) -> None:
        """Stellt sicher, dass das Database-Verzeichnis existiert"""
        db_dir = Path(self.db_path).parent
        if not db_dir.exists():
            try:
                db_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created database directory: {db_dir}")
            except OSError as e:
                logger.error(f"Failed to create database directory {db_dir}: {e}")
                raise

    def _get_connection(self) -> sqlite3.Connection:
        """Holt oder erstellt eine thread-lokale Verbindung"""
        if not hasattr(self._local, "connection") or self._local.connection is None:
            try:
                # Absoluten Pfad verwenden für bessere Kompatibilität
                abs_path = Path(self.db_path).resolve()
                self._local.connection = sqlite3.connect(
                    str(abs_path),
                    check_same_thread=False,  # Erlaubt thread-übergreifende Nutzung
                    timeout=30.0,
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                )
                self._local.connection.row_factory = sqlite3.Row
                # Optimierungen für bessere Performance
                self._local.connection.execute("PRAGMA journal_mode=WAL")
                self._local.connection.execute("PRAGMA synchronous=NORMAL")
                self._local.connection.execute("PRAGMA cache_size=1000")
                self._local.connection.execute("PRAGMA temp_store=MEMORY")
                logger.debug(f"New SQLite connection created for thread: {abs_path}")
            except sqlite3.Error as e:
                logger.error(f"Failed to connect to SQLite database at {abs_path}: {e}")
                raise
        return self._local.connection

    def connect(self) -> None:
        """Initialisiert die thread-lokale Verbindung"""
        try:
            self._get_connection()  # Entfernt das unbenutzte 'conn'
            logger.info(f"Connected to SQLite database: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to connect to SQLite database: {e}")
            raise

    def disconnect(self) -> None:
        """Schließt die thread-lokale Verbindung"""
        if hasattr(self._local, "connection") and self._local.connection:
            try:
                self._local.connection.close()
                self._local.connection = None
                logger.debug("SQLite connection closed for thread")
            except Exception as e:
                logger.warning(f"Error closing SQLite connection: {e}")

    def create_user_table(self) -> None:
        """User-Tabelle erstellen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS users
                        (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            password_hash TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )
                """
            )
            conn.commit()
            logger.info("User table created/verified")
        except Exception as e:
            logger.error(f"Failed to create user table: {e}")
            raise
        finally:
            cursor.close()

    def create_user(self, username: str, email: str, password_hash: str) -> bool:
        """Neuen User erstellen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash),
            )
            conn.commit()
            logger.info(f"User created successfully: {email}")
            return True
        except sqlite3.IntegrityError as e:
            logger.warning(f"User creation failed (duplicate): {e}")
            conn.rollback()
            return False
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """User anhand Email suchen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, username, email, password_hash, created_at FROM users WHERE email = ?",
                (email,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get user by email: {e}")
            raise
        finally:
            cursor.close()

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """User anhand Username suchen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, username, email, password_hash, created_at FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get user by username: {e}")
            raise
        finally:
            cursor.close()

    def get_password_hash_by_email(self, email: str) -> Optional[str]:
        """Password-Hash für Email abrufen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            return row if row else None
        except Exception as e:
            logger.error(f"Failed to get password hash by email: {e}")
            raise
        finally:
            cursor.close()

    def update_user_password(self, email: str, new_password_hash: str) -> bool:
        """Passwort aktualisieren"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE email = ?",
                (new_password_hash, email),
            )
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Password updated for user: {email}")
            return success
        except Exception as e:
            logger.error(f"Failed to update password: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()

    def delete_user(self, email: str) -> bool:
        """User löschen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE email = ?", (email,))
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"User deleted: {email}")
            return success
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
