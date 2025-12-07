from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector


def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, fast, free
    text = "This is an example sentence."
    emb = model.encode(text).tolist()  # convert to Python list for DB storage
    print(len(emb), emb[:5])


if __name__ == "__main__":
    main()
