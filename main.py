from src.embeddings import EmbeddingGenerator
from src.configuration import Configuration

config = Configuration()


def main():
    """Main function to run the embedding generation job."""
    print(config)
    generator = EmbeddingGenerator()
    generator.process_documents()


if __name__ == "__main__":
    main()
