"""
Moduł zarządzania połączeniem z bazą danych PostgreSQL.

Ten plik zawiera klasę DatabaseConfig, która:
1. Ładuje konfigurację z pliku .env
2. Tworzy połączenia do bazy danych
3. Automatycznie włącza rozszerzenie pgvector
4. Zapewnia bezpieczne zamykanie połączeń
"""

import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.configuration import Configuration
import psycopg2
from psycopg2 import pool

config = Configuration()


class DatabaseConfig:
    """
    Klasa do zarządzania konfiguracją i połączeniami z PostgreSQL.

    Attributes:
        host (str): Adres hosta bazy danych (np. 'localhost')
        port (str): Port bazy danych (domyślnie '5432')
        database (str): Nazwa bazy danych
        user (str): Nazwa użytkownika PostgreSQL
        password (str): Hasło użytkownika
    """

    def __init__(self):
        """
        Inicjalizacja konfiguracji z zmiennych środowiskowych.
        Jeśli zmienna nie istnieje, używa wartości domyślnej.
        """
        self.host = config.db.postgres_host
        self.port = config.db.postgres_port
        self.database = config.db.postgres_db
        self.user = config.db.postgres_user
        self.password = config.db.postgres_password

    def get_connection(self):
        """Get a synchronous database connection."""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.database,
        )

    def get_pool(self):
        """Get a synchronous connection pool."""
        # For simple synchronous usage, just return a connection
        # For more advanced pooling, could use psycopg2.pool
        return pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}",
        )

    def get_sessionmaker(self):
        """
        Tworzy i zwraca połączenie z bazą danych PostgreSQL.

        RealDictCursor sprawia, że wyniki zapytań są zwracane jako słowniki,
        co ułatwia dostęp do kolumn po nazwie (np. row['filename'])

        Returns:
            psycopg2.connection: Aktywne połączenie z bazą danych

        Raises:
            Exception: Jeśli połączenie się nie powiedzie
        """
        try:
            dsn = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            engine = create_async_engine(dsn, echo=False)

            return async_sessionmaker(bind=engine, expire_on_commit=False)

        except Exception as e:
            raise Exception(f"❌ Nie udało się połączyć z bazą danych: {str(e)}")

    def close_connection(self, conn):
        """
        Bezpiecznie zamyka połączenie z bazą danych.

        Args:
            conn: Połączenie do zamknięcia
        """
        if conn:
            conn.close()


# Globalna instancja konfiguracji - używana w innych modułach
db_config = DatabaseConfig()
