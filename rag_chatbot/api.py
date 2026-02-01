"""FastAPI service for the RAG chatbot."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .chat import generate_answer
from .config import AppConfig
from .gcp import initialize_vertex_ai
from .retrieval import retrieve_context


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


app = FastAPI(title="RAG Chatbot", version="0.1.0")


@app.get("/healthz")
def health_check() -> dict[str, str]:
    config = AppConfig.from_env()
    missing = config.validate()
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required environment variables: {', '.join(missing)}",
        )
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    config = AppConfig.from_env()
    missing = config.validate()
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required environment variables: {', '.join(missing)}",
        )
    initialize_vertex_ai(config)
    chunks = retrieve_context(config, request.query, top_k=request.top_k)
    response = generate_answer(config, request.query, chunks)
    sources = [chunk.uri for chunk in response.sources]
    return ChatResponse(answer=response.answer, sources=sources)
