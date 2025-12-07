from typing import List
from pydantic import BaseModel, Field
from google.adk.tools import FunctionTool
from src.embeddings import EmbeddingStore


class EmbeddingField(BaseModel):
    """Embedding search result field - simplified for Google ADK compatibility."""

    id: int = Field(default=0, description="Unique identifier for the embedding")
    content: str = Field(description="The content/text of the embedding")
    similarity: float = Field(
        default=0.0, description="Similarity score between 0 and 1"
    )


class EmbeddingsSearchOutput(BaseModel):
    embeddings: List[EmbeddingField]


def embeddings_search(query: str) -> EmbeddingsSearchOutput:
    """Search for embeddings related to the query and return structured results."""
    try:
        store = EmbeddingStore()
        store.init()
        results = store.search(query)

        # Convert results to EmbeddingField objects, handling None values
        embeddings = []
        for result in results:
            try:
                embedding = EmbeddingField(
                    id=result.get("id", 0) or 0,  # Handle None values
                    content=result.get("content", "") or "",
                    similarity=float(result.get("similarity", 0.0) or 0.0),
                )
                embeddings.append(embedding)
            except (ValueError, TypeError) as e:
                # Skip malformed results
                continue

        return EmbeddingsSearchOutput(embeddings=embeddings)

    except Exception as e:
        # Return empty results on error to maintain JSON structure
        return EmbeddingsSearchOutput(embeddings=[])


embeddings_search_tool = FunctionTool(func=embeddings_search)
