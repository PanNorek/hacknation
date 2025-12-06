"""
Moduł zarządzania połączeniem z bazą danych PostgreSQL.

Ten plik zawiera klasę DatabaseConfig, która:
1. Ładuje konfigurację z pliku .env
2. Tworzy połączenia do bazy danych
3. Automatycznie włącza rozszerzenie pgvector
4. Zapewnia bezpieczne zamykanie połączeń
"""

# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.configuration import Configuration


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
            dsn = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            engine = create_engine(dsn)

            return sessionmaker(bind=engine)

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
