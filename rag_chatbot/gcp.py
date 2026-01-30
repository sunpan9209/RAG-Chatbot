"""Helpers for working with Google Cloud resources."""

from __future__ import annotations

from typing import Optional

from google.cloud import aiplatform

from .config import AppConfig


def initialize_vertex_ai(config: AppConfig) -> None:
    """Initialize the Vertex AI SDK with the configured project settings."""
    aiplatform.init(project=config.gcp_project_id, location=config.gcp_region)


def get_endpoint_resource_id(endpoint_name: str) -> Optional[str]:
    """Extract a numeric endpoint ID from a full endpoint name."""
    parts = endpoint_name.split("/")
    if not parts:
        return None
    return parts[-1] or None
