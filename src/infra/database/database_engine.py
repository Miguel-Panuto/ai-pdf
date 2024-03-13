from os import environ

import psycopg2


class DatabaseEngine:
    def __init__(self):
        url = environ.get('POSTGRES_URL')
        if url is None:
            raise Exception('POSTGRES_URL environment variable is not set')
        self._con = psycopg2.connect(url)
        self.cursor = self._con.cursor()

    def sql_one(self, query: str, *args) -> tuple:
        self.cursor.execute(query, args)
        self._con.commit()
        result = self.cursor.fetchone()
        if result is None:
            raise Exception('No result found')
        return result

    def sql_all(self, query: str, *args) -> list[tuple]:
        self.cursor.execute(query, args)
        self._con.commit()
        return self.cursor.fetchall()
    
    def _close_cursor(self) -> None:
        self.cursor.close()

    def __del__(self) -> None:
        if self._con:
            self._con.close()
        if self.cursor:
            self.cursor.close()
