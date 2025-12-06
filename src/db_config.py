"""
Moduł zarządzania połączeniem z bazą danych PostgreSQL.

Ten plik zawiera klasę DatabaseConfig, która:
1. Ładuje konfigurację z pliku .env
2. Tworzy połączenia do bazy danych
3. Automatycznie włącza rozszerzenie pgvector
4. Zapewnia bezpieczne zamykanie połączeń
"""

import os
from typing import Optional

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()


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
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.database = os.getenv("POSTGRES_DB", "hacknation")
        self.user = os.getenv("POSTGRES_USER", "postgres")
        self.password = os.getenv("POSTGRES_PASSWORD", "")
    
    def get_connection(self):
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
            # Nawiązanie połączenia
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor  # Wyniki jako słowniki
            )
            
            # Włączenie rozszerzenia pgvector (jeśli jeszcze nie istnieje)
            with conn.cursor() as cursor:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            conn.commit()
            
            return conn
            
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