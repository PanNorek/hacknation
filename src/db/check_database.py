"""
Skrypt do sprawdzania zawartości bazy danych.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from db_config import db_config


def check_database():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    try:
        print("\n" + "="*80)
        print("📊 RAPORT BAZY DANYCH")
        print("="*80 + "\n")
        
        # Statystyki
        cursor.execute('SELECT COUNT(*) FROM documents;')
        total = cursor.fetchone()[0]
        print(f"✅ Dokumentów w bazie: {total}")
        
        if total == 0:
            print("\n⚠️  Baza jest pusta!")
            print("💡 Uruchom: python main_pipeline.py")
            return
        
        cursor.execute('SELECT COUNT(*) FROM documents WHERE embedding IS NOT NULL;')
        with_emb = cursor.fetchone()[0]
        print(f"🧠 Dokumentów z embeddingami: {with_emb}/{total}")
        
        # Lista dokumentów
        print("\n" + "="*80)
        print("📚 LISTA DOKUMENTÓW")
        print("="*80 + "\n")
        
        cursor.execute('''
            SELECT 
                id,
                filename,
                LEFT(summary, 100) as preview,
                created_at
            FROM documents
            ORDER BY created_at DESC;
        ''')
        
        docs = cursor.fetchall()
        for i, doc in enumerate(docs, 1):
            print(f"{i}. 📄 {doc[1]}")
            print(f"   📝 {doc[2]}...")
            print(f"   📅 {doc[3]}")
            print()
        
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    check_database()