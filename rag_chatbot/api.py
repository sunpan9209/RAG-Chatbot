"""FastAPI service for the RAG chatbot."""

from __future__ import annotations

from dataclasses import asdict
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .chat import generate_answer
from .config import AppConfig
from .indexing import build_vector_index_from_gcs, load_vector_index, save_vector_index
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


class IndexRequest(BaseModel):
    prefix: str | None = None
    overwrite: bool = True


class IndexResponse(BaseModel):
    indexed_documents: int
    index_uri: str


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


@app.post("/index", response_model=IndexResponse)
def index_documents(request: IndexRequest) -> IndexResponse:
    config = _load_config()
    if not request.overwrite:
        existing = load_vector_index(config, config.vector_index_path)
        if existing.entries:
            raise HTTPException(
                status_code=409,
                detail="Vector index already exists. Set overwrite=true to replace it.",
            )
    index = build_vector_index_from_gcs(config, prefix=request.prefix)
    save_vector_index(config, index, config.vector_index_path)
    indexed_docs = {entry.uri.split("#", 1)[0] for entry in index.entries}
    return IndexResponse(indexed_documents=len(indexed_docs), index_uri=config.vector_index_path)
