import asyncio
from src.embeddings import EmbeddingGenerator
from src.configuration import Configuration

config = Configuration()


async def main():
    """Main function to run the embedding generation job."""
    print(config)
    generator = EmbeddingGenerator()
    await generator.process_documents()


if __name__ == "__main__":
    asyncio.run(main())
