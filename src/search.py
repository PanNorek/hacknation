"""
Moduł do wyszukiwania semantycznego używając pgvector.
"""
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from db_config import db_config


class SemanticSearch:
    """
    Klasa do wyszukiwania semantycznego w bazie dokumentów.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Inicjalizacja wyszukiwarki.
        
        Args:
            model_name: Nazwa modelu (musi być taka sama jak w embeddings.py!)
        """
        print(f"🔍 Ładowanie modelu do wyszukiwania: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("✅ Model załadowany!\n")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Wykonuje wyszukiwanie semantyczne dla zapytania.
        
        Args:
            query: Zapytanie użytkownika (np. "dokumenty finansowe")
            top_k: Liczba wyników do zwrócenia
            
        Returns:
            Lista słowników z wynikami: {filename, summary, similarity}
        """
        # Krok 1: Generuj embedding dla zapytania
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        query_embedding_list = query_embedding.tolist()
        
        # Krok 2: Wyszukaj podobne dokumenty używając pgvector
        conn = db_config.get_connection()
        cursor = conn.cursor()
        
        try:
            # Użyj pgvector do wyszukiwania cosine similarity
            # <=> operator to cosine distance w pgvector
            cursor.execute("""
                SELECT 
                    id,
                    filename,
                    summary,
                    1 - (embedding <=> %s) as similarity
                FROM documents
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s;
            """, (query_embedding_list, query_embedding_list, top_k))
            
            results = cursor.fetchall()
            
            # Konwertuj na listę słowników
            return [
                {
                    "id": row[0],
                    "filename": row[1],
                    "summary": row[2],
                    "similarity": float(row[3])
                }
                for row in results
            ]
            
        finally:
            cursor.close()
            db_config.close_connection(conn)


def main():
    """Przykład użycia wyszukiwarki."""
    print("=" * 80)
    print("🔍 TEST WYSZUKIWANIA SEMANTYCZNEGO")
    print("=" * 80)
    print()
    
    # Inicjalizuj wyszukiwarkę
    search = SemanticSearch()
    
    # Przykładowe zapytania
    queries = [
        "dokumenty finansowe i raporty",
        "umowy prawne",
        "dokumentacja techniczna",
    ]
    
    for query in queries:
        print(f"\n{'='*80}")
        print(f"🔍 Zapytanie: '{query}'")
        print('='*80)
        
        results = search.search(query, top_k=3)
        
        if not results:
            print("  ❌ Brak wyników")
            continue
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. 📄 {result['filename']}")
            print(f"   🎯 Podobieństwo: {result['similarity']:.4f}")
            print(f"   📝 Streszczenie: {result['summary'][:150]}...")
    
    print("\n" + "="*80)
    print("✅ TEST ZAKOŃCZONY")
    print("="*80)


if __name__ == "__main__":
    main()