# database_connector.py
from mock_database import MockDatabase

# Singleton pattern - one database instance for the whole app
class DatabaseConnector:
    _instance = None
    
    @staticmethod
    def get_instance():
        if DatabaseConnector._instance is None:
            DatabaseConnector._instance = MockDatabase()
        return DatabaseConnector._instance