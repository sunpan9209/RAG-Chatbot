"""Document ingestion pipeline skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from google.cloud import storage

from .config import AppConfig


@dataclass(frozen=True)
class IngestionResult:
    uploaded: list[str]


def upload_documents(config: AppConfig, source_paths: Iterable[Path]) -> IngestionResult:
    """Upload local documents to the configured GCS bucket."""
    client = storage.Client(project=config.gcp_project_id)
    bucket = client.bucket(config.document_bucket)

    uploaded: list[str] = []
    for path in source_paths:
        blob = bucket.blob(path.name)
        blob.upload_from_filename(path)
        uploaded.append(f"gs://{config.document_bucket}/{path.name}")

    return IngestionResult(uploaded=uploaded)
