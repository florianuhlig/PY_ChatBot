import logging
from typing import Dict, Any
from .interface import DatabaseInterface
from .sqlite_db import SQLiteDatabase

logger = logging.getLogger(__name__)


class DatabaseFactory:

    @staticmethod
    def create_database(db_type: str, config: Dict[str, Any]) -> DatabaseInterface:

        if db_type.lower() == 'sqlite':
            if 'path' not in config:
                raise ValueError("SQLite configuration requires 'path'")
            return SQLiteDatabase(config['path'])

        elif db_type.lower() == 'mysql':
            # Für später: MySQL-Implementierung
            # from .mysql_db import MySQLDatabase
            # return MySQLDatabase(config)
            raise NotImplementedError("MySQL support not yet implemented")

        elif db_type.lower() == 'postgresql':
            # Für später: PostgreSQL-Implementierung
            # from .postgresql_db import PostgreSQLDatabase
            # return PostgreSQLDatabase(config)
            raise NotImplementedError("PostgreSQL support not yet implemented")

        else:
            raise ValueError(f"Unsupported database type: {db_type}")


# Convenience-Funktion für einfachen Zugriff
def get_database(db_type: str, config: Dict[str, Any]) -> DatabaseInterface:
    db = DatabaseFactory.create_database(db_type, config)
    db.connect()
    db.create_user_table()
    return db
