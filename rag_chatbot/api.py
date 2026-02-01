"""FastAPI service for the RAG chatbot."""

from __future__ import annotations

from dataclasses import asdict
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .chat import generate_answer
from .config import AppConfig
from .retrieval import RetrievedChunk, retrieve_context

app = FastAPI(title="RAG Chatbot API")


class ChatRequest(BaseModel):
    query: str


class Source(BaseModel):
    uri: str
    content: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]


def _load_config() -> AppConfig:
    config = AppConfig.from_env()
    missing = config.validate()
    if missing:
        missing_vars = ", ".join(missing)
        raise HTTPException(
            status_code=400,
            detail=f"Missing required environment variables: {missing_vars}",
        )
    return config


@app.get("/healthz")
def healthz() -> dict[str, str]:
    _load_config()
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    config = _load_config()
    chunks = retrieve_context(config, request.query)
    response = generate_answer(config, request.query, chunks)
    sources = [Source(**asdict(chunk)) for chunk in response.sources]
    return ChatResponse(answer=response.answer, sources=sources)
