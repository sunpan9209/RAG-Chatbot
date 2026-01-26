"""Command-line entry points for the RAG chatbot."""

from __future__ import annotations

import argparse
from pathlib import Path

from .chat import generate_answer
from .config import AppConfig
from .ingest import upload_documents
from .retrieval import retrieve_context


def run_health_check() -> int:
    config = AppConfig.from_env()
    missing = config.validate()
    if missing:
        missing_vars = ", ".join(missing)
        print(f"Missing required environment variables: {missing_vars}")
        return 1
    print("Configuration looks good.")
    return 0


def run_ingest(paths: list[Path]) -> int:
    config = AppConfig.from_env()
    missing = config.validate()
    if missing:
        missing_vars = ", ".join(missing)
        print(f"Missing required environment variables: {missing_vars}")
        return 1
    result = upload_documents(config, paths)
    print("Uploaded documents:")
    for uri in result.uploaded:
        print(f"- {uri}")
    return 0


def run_chat(query: str) -> int:
    config = AppConfig.from_env()
    missing = config.validate()
    if missing:
        missing_vars = ", ".join(missing)
        print(f"Missing required environment variables: {missing_vars}")
        return 1
    chunks = retrieve_context(query)
    response = generate_answer(config, query, chunks)
    print(response.answer)
    if response.sources:
        print("\nSources:")
        for chunk in response.sources:
            print(f"- {chunk.uri}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RAG Chatbot CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health", help="Validate configuration")

    ingest_parser = subparsers.add_parser("ingest", help="Upload documents to GCS")
    ingest_parser.add_argument("paths", nargs="+", type=Path)

    chat_parser = subparsers.add_parser("chat", help="Run a test query")
    chat_parser.add_argument("query")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "health":
        return run_health_check()
    if args.command == "ingest":
        return run_ingest(args.paths)
    if args.command == "chat":
        return run_chat(args.query)
    raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
