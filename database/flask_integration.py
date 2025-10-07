import logging

from flask import g

from .interface import DatabaseInterface

logger = logging.getLogger(__name__)


class FlaskDatabaseManager:
    """Flask-Integration für Thread-Safe Database Management"""

    def __init__(self, database_factory_func):
        self.database_factory_func = database_factory_func

    def get_db(self) -> DatabaseInterface:
        """
        Holt die Datenbank-Instanz für den aktuellen Request
        Verwendet Flask's 'g' object für request-lokale Speicherung
        """
        if "database" not in g:
            g.database = self.database_factory_func()
            g.database.connect()
            g.database.create_user_table()
            logger.debug("Database instance created for request")

        return g.database

    def close_db(self, error=None):
        """
        Schließt die Datenbank-Verbindung am Ende des Requests
        """
        database = g.pop("database", None)
        if database is not None:
            database.disconnect()
            logger.debug("Database connection closed for request")

    def init_app(self, app):
        """Registriert die Database-Manager-Funktionen bei Flask"""
        app.teardown_appcontext(self.close_db)
