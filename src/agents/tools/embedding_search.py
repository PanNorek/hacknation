from typing import List
from pydantic import BaseModel
from google.adk.tools import FunctionTool
from src.embeddings import EmbeddingStore


class EmbeddingField(BaseModel):
    id: int
    content: str
    similarity: float


class EmbeddingsSearchOutput(BaseModel):
    embeddings: List[EmbeddingField]


def embeddings_search(query: str) -> EmbeddingsSearchOutput:
    store = EmbeddingStore()
    store.init()
    results = store.search(query)
    return EmbeddingsSearchOutput(
        embeddings=[EmbeddingField(**result) for result in results]
    )


embeddings_search_tool = FunctionTool(func=embeddings_search)
