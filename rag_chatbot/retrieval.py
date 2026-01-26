"""Retrieval component skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RetrievedChunk:
    uri: str
    content: str
    score: float


def retrieve_context(query: str, *, top_k: int = 5) -> Iterable[RetrievedChunk]:
    """Placeholder retrieval implementation."""
    return [
        RetrievedChunk(uri="stub://example", content=f"Stub context for {query}", score=1.0)
    ][:top_k]
