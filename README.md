# RAG-Chatbot

RAG based chatbot starter project with Google Cloud integration stubs.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Set environment variables:

```bash
export GCP_PROJECT_ID="rag-chatbot-485501"
export GCP_REGION="us-central1"
export DOCUMENT_BUCKET="llm-doc-bucket"
```

Validate configuration:

```bash
rag-chatbot health
```

Upload documents:

```bash
rag-chatbot ingest path/to/doc1.pdf path/to/doc2.txt
```

Run a test query (stub response until Vertex AI wiring is implemented):

```bash
rag-chatbot chat "What is in the docs?"
```

## Implementation Phases

1. **Foundation (this commit)**
   - Configuration, CLI entry points, and stubs for ingestion, retrieval, and chat orchestration.
2. **Retrieval pipeline**
   - Add document parsing, embedding generation, and vector index creation.
3. **Answer generation**
   - Replace stub response with a Vertex AI (Gemini) model invocation (this project uses
     Gemini, not OpenAI).
4. **Deployment**
   - Add service layer (FastAPI/Cloud Run) and CI/CD workflows.

## Notes

- The current modules are scaffolding; connect them to your chosen data store and models.
- Update dependencies as needed once the detailed design is confirmed.
