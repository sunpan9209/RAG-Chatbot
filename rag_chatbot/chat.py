"""Chat orchestration skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .config import AppConfig
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
    """Stub answer generation."""
    prompt = build_prompt(query, chunks)
    answer = (
        "Stub response. Replace with a call to Vertex AI using model "
        f"{config.chat_model}. Prompt length: {len(prompt)}"
    )
    return ChatResponse(answer=answer, sources=chunks)
