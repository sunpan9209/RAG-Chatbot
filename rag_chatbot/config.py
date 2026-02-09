"""Configuration management for the RAG chatbot."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """Application configuration sourced from environment variables.

    Note: The default model assumes Vertex AI (Gemini). This project uses Gemini;
    OpenAI is not wired.
    """

    gcp_project_id: str
    gcp_region: str
    chat_model: str
    document_bucket: str
    vector_index_path: str

    @staticmethod
    def from_env() -> "AppConfig":
        return AppConfig(
            gcp_project_id=os.environ.get("GCP_PROJECT_ID", ""),
            gcp_region=os.environ.get("GCP_REGION", "us-central1"),
            chat_model=os.environ.get("CHAT_MODEL", "gemini-2.5-pro"),
            document_bucket=os.environ.get("DOCUMENT_BUCKET", ""),
            vector_index_path=os.environ.get("VECTOR_INDEX_PATH", "vector_index.jsonl"),
        )

    def validate(self) -> list[str]:
        """Return a list of missing required settings."""
        missing = []
        if not self.gcp_project_id:
            missing.append("GCP_PROJECT_ID")
        if not self.document_bucket:
            missing.append("DOCUMENT_BUCKET")
        return missing
