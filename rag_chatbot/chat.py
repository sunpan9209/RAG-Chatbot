"""Chat orchestration skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .config import AppConfig
from .gcp import initialize_vertex_ai
from .retrieval import RetrievedChunk


@dataclass(frozen=True)
class ChatResponse:
    answer: str
    sources: Iterable[RetrievedChunk]


def build_prompt(query: str, chunks: Iterable[RetrievedChunk]) -> str:
    context = "\n\n".join(chunk.content for chunk in chunks)
    return (
        "You are a helpful assistant. Use the following context to answer the question.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )


def generate_answer(
    config: AppConfig,
    query: str,
    chunks: Iterable[RetrievedChunk],
) -> ChatResponse:
    """Generate an answer using Vertex AI Gemini."""
    initialize_vertex_ai(config)
    prompt = build_prompt(query, chunks)
    from vertexai.preview.generative_models import GenerativeModel

    model = GenerativeModel(config.chat_model)
    response = model.generate_content(prompt)
    answer = response.text or ""
    return ChatResponse(answer=answer, sources=chunks)
