"""Embedding helpers for Vertex AI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .config import AppConfig
from .gcp import initialize_vertex_ai


@dataclass(frozen=True)
class VertexEmbeddingClient:
    """Client wrapper for generating text embeddings."""

    config: AppConfig

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        initialize_vertex_ai(self.config)
        from vertexai.preview.language_models import TextEmbeddingModel

        model = TextEmbeddingModel.from_pretrained(self.config.embedding_model)
        embeddings = model.get_embeddings(texts)
        return [embedding.values for embedding in embeddings]


def chunk_text(text: str, *, chunk_size: int = 1500) -> Iterable[str]:
    """Yield fixed-size chunks of text for embedding."""
    for start in range(0, len(text), chunk_size):
        yield text[start : start + chunk_size]
