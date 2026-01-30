"""Retrieval component skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from pathlib import Path
from typing import Iterable

from .config import AppConfig
from .embeddings import VertexEmbeddingClient
from .indexing import VectorIndex


@dataclass(frozen=True)
class RetrievedChunk:
    uri: str
    content: str
    score: float


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def retrieve_context(
    config: AppConfig, query: str, *, top_k: int = 5
) -> Iterable[RetrievedChunk]:
    """Retrieve top-k chunks from the local JSONL vector index."""
    index_path = Path(config.vector_index_path)
    index = VectorIndex.load(index_path)
    if not index.entries:
        return []

    client = VertexEmbeddingClient(config)
    query_embedding = client.embed_texts([query])[0]

    scored = [
        RetrievedChunk(
            uri=entry.uri,
            content=entry.content,
            score=_cosine_similarity(query_embedding, entry.embedding),
        )
        for entry in index.entries
    ]
    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:top_k]
