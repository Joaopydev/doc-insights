from typing import Optional
from psycopg import connect, Connection

from src.main.config.settings import settings


class NeonConnection:

    _connection: Optional[Connection] = None

    @classmethod
    def get_connection(cls) -> Connection:

        if cls._connection is None or cls._connection.closed:
            cls._connection = connect(settings.neon_database_url)

        return cls._connection
