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

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(asdict(entry)) for entry in self.entries) + "\n"

    def save(self, path: Path) -> None:
        with path.open("w", encoding="utf-8") as handle:
            handle.write(self.to_jsonl())

    @staticmethod
    def load(path: Path) -> "VectorIndex":
        if not path.exists():
            return VectorIndex(entries=[])
        return VectorIndex.from_jsonl(path.read_text(encoding="utf-8"))

    @staticmethod
    def from_jsonl(payload: str) -> "VectorIndex":
        entries: list[IndexEntry] = []
        for line in payload.splitlines():
            if not line.strip():
                continue
            entries.append(IndexEntry(**json.loads(line)))
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


def _load_storage_client(config: AppConfig):
    from google.cloud import storage

    return storage.Client(project=config.gcp_project_id)


def _is_gcs_uri(value: str) -> bool:
    return value.startswith("gs://")


def _parse_gcs_uri(uri: str) -> tuple[str, str]:
    if not uri.startswith("gs://"):
        raise ValueError(f"Not a GCS URI: {uri}")
    bucket_name, _, blob_name = uri[5:].partition("/")
    if not bucket_name or not blob_name:
        raise ValueError(f"Invalid GCS URI: {uri}")
    return bucket_name, blob_name


def load_vector_index(config: AppConfig, path_value: str) -> VectorIndex:
    if _is_gcs_uri(path_value):
        bucket_name, blob_name = _parse_gcs_uri(path_value)
        client = _load_storage_client(config)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        if not blob.exists():
            return VectorIndex(entries=[])
        content = blob.download_as_text()
        return VectorIndex.from_jsonl(content)
    return VectorIndex.load(Path(path_value))


def save_vector_index(config: AppConfig, index: VectorIndex, path_value: str) -> None:
    if _is_gcs_uri(path_value):
        bucket_name, blob_name = _parse_gcs_uri(path_value)
        client = _load_storage_client(config)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(index.to_jsonl(), content_type="application/json")
        return
    output_path = Path(path_value)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    index.save(output_path)


def build_vector_index_from_gcs(
    config: AppConfig, *, prefix: str | None = None
) -> VectorIndex:
    client = _load_storage_client(config)
    bucket = client.bucket(config.document_bucket)
    index_bucket: str | None = None
    index_blob: str | None = None
    if _is_gcs_uri(config.vector_index_path):
        index_bucket, index_blob = _parse_gcs_uri(config.vector_index_path)
    entries: list[IndexEntry] = []
    embedder = VertexEmbeddingClient(config)
    for blob in client.list_blobs(bucket, prefix=prefix):
        if blob.name.endswith("/"):
            continue
        if index_bucket == config.document_bucket and blob.name == index_blob:
            continue
        text = blob.download_as_bytes().decode("utf-8", errors="ignore")
        for chunk_id, chunk in enumerate(chunk_text(text)):
            embedding = embedder.embed_texts([chunk])[0]
            uri = f"gs://{config.document_bucket}/{blob.name}#chunk={chunk_id}"
            entries.append(IndexEntry(uri=uri, content=chunk, embedding=embedding))
    return VectorIndex(entries=entries)
