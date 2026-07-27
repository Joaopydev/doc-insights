# pylint: disable=no-member
from typing import Optional
from psycopg import connect, Connection
from pgvector.psycopg import register_vector

from src.main.config.settings import settings


class VectorDatabaseConnection:

    def __init__(self):
        self.connection: Optional[Connection] = None

    def __enter__(self) -> Connection:
        self.connection = connect(settings.neon_database_url)
        register_vector(self.connection)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection is None:
            return

        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()

        self.connection.close()
