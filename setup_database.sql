-- =====================================================
-- KROK 1: Włączenie rozszerzenia pgvector
-- =====================================================
-- pgvector pozwala przechowywać i wyszukiwać wektory (embeddingi)
-- w PostgreSQL używając operacji similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- =====================================================
-- KROK 2: Utworzenie tabeli documents
-- =====================================================
-- Tabela przechowuje:
-- - id: unikalny identyfikator dokumentu
-- - filename: nazwa pliku PDF (np. "dokument.pdf")
-- - raw_text: pełny wyekstraktowany tekst z PDF
-- - summary: wygenerowane streszczenie przez Gemini
-- - embedding: wektor 384-wymiarowy (embeddingi z sentence-transformers)
-- - created_at/updated_at: timestamps do śledzenia zmian
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL UNIQUE,
    raw_text TEXT,
    summary TEXT,
    embedding vector(384),  -- 384 wymiary dla modelu all-MiniLM-L6-v2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- KROK 3: Utworzenie indeksu dla szybkiego wyszukiwania
-- =====================================================
-- IVFFLAT (Inverted File with Flat compression) to algorytm
-- przyspieszający wyszukiwanie wektorów przez cosine similarity
-- lists=100 oznacza podział przestrzeni na 100 klastrów
CREATE INDEX IF NOT EXISTS documents_embedding_idx 
ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- =====================================================
-- KROK 4: Automatyczna aktualizacja pola updated_at
-- =====================================================
-- Funkcja która automatycznie ustawia current timestamp
-- przy każdej aktualizacji rekordu
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger wywołujący funkcję przed każdym UPDATE
CREATE TRIGGER update_documents_updated_at 
BEFORE UPDATE ON documents 
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- GOTOWE! Baza danych jest skonfigurowana
-- =====================================================