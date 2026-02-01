"""Simple JSONL-based vector index for retrieval."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable

from .embeddings import VertexEmbeddingClient, chunk_text
from .config import AppConfig


@dataclass(frozen=True)
class IndexEntry:
    uri: str
    content: str
    embedding: list[float]


@dataclass
class VectorIndex:
    entries: list[IndexEntry]

    def save(self, path: Path) -> None:
        with path.open("w", encoding="utf-8") as handle:
            for entry in self.entries:
                handle.write(json.dumps(asdict(entry)) + "\n")

    @staticmethod
    def load(path: Path) -> "VectorIndex":
        entries: list[IndexEntry] = []
        if not path.exists():
            return VectorIndex(entries=entries)
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                payload = json.loads(line)
                entries.append(IndexEntry(**payload))
        return VectorIndex(entries=entries)


def build_vector_index(
    config: AppConfig,
    source_paths: Iterable[Path],
    output_path: Path,
) -> VectorIndex:
    """Create a JSONL vector index from local documents."""
    client = VertexEmbeddingClient(config)
    entries: list[IndexEntry] = []

    for path in source_paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for chunk_id, chunk in enumerate(chunk_text(text)):
            embedding = client.embed_texts([chunk])[0]
            uri = f"{path.as_posix()}#chunk={chunk_id}"
            entries.append(IndexEntry(uri=uri, content=chunk, embedding=embedding))

    index = VectorIndex(entries=entries)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    index.save(output_path)
    return index
