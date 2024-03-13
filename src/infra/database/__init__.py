from .database_engine import DatabaseEngine

database_engine: DatabaseEngine

def instantiate_database_engine():
    global database_engine
    database_engine = DatabaseEngine()

def unload_database_engine():
    global database_engine
    del database_engine
    database_engine = None # type: ignore
