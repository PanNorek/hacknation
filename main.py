import asyncio
from src.embeddings import EmbeddingGenerator, EmbeddingStore
from src.configuration import Configuration

config = Configuration()


async def main():
    """Main function to run the embedding generation job."""
    # print(config)
    # generator = EmbeddingGenerator()
    # await generator.process_documents()

    store = EmbeddingStore()
    store.init()
    results = store.search("Polska")
    print("\n\n".join(str(result) for result in results))


if __name__ == "__main__":
    asyncio.run(main())
