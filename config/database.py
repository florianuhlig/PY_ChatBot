import os
from typing import Any, Dict


class DatabaseConfig:
    def __init__(self):
        # Environment-basierte Konfiguration
        self.db_type = os.getenv("DB_TYPE", "sqlite")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if self.db_type.lower() == "sqlite":
            return {"path": os.getenv("SQLITE_PATH", "databases/chatbot.db")}
        elif self.db_type.lower() == "mysql":
            return {
                "host": os.getenv("MYSQL_HOST", "localhost"),
                "port": int(os.getenv("MYSQL_PORT", "3306")),
                "database": os.getenv("MYSQL_DATABASE", "chatbot"),
                "user": os.getenv("MYSQL_USER", "root"),
                "password": os.getenv("MYSQL_PASSWORD", ""),
                "charset": "utf8mb4",
            }
        elif self.db_type.lower() == "mariadb":
            return {
                "host": os.getenv("MARIADB_HOST", "localhost"),
                "port": int(os.getenv("MARIADB_PORT", "3306")),
                "database": os.getenv("MARIADB_DATABASE", "chatbot"),
                "user": os.getenv("MARIADB_USER", "root"),
                "password": os.getenv("MARIADB_PASSWORD", ""),
                "charset": "utf8",
            }
        elif self.db_type.lower() == "postgresql":
            return {
                "host": os.getenv("POSTGRES_HOST", "localhost"),
                "port": int(os.getenv("POSTGRES_PORT", "5432")),
                "database": os.getenv("POSTGRES_DATABASE", "chatbot"),
                "user": os.getenv("POSTGRES_USER", "postgres"),
                "password": os.getenv("POSTGRES_PASSWORD", ""),
            }
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def get_database_config(self) -> tuple[str, Dict[str, Any]]:
        return self.db_type, self.config
