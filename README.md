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
export VECTOR_INDEX_PATH="vector_index.jsonl"
```

Validate configuration:

```bash
rag-chatbot health
```

Upload documents:

```bash
rag-chatbot ingest path/to/doc1.pdf path/to/doc2.txt
```

Build a local vector index (JSONL):

```bash
rag-chatbot index path/to/doc1.txt path/to/doc2.txt
```

Run a test query:

```bash
rag-chatbot chat "What is in the docs?"
```

## API Service (Next Step)

Run the FastAPI service locally:

```bash
uvicorn rag_chatbot.api:app --host 0.0.0.0 --port 8080
```

Example request:

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarize the docs", "top_k": 5}'
```

## Implementation Phases

1. **Foundation (this commit)**
   - Configuration, CLI entry points, and stubs for ingestion, retrieval, and chat orchestration.
2. **Retrieval pipeline**
   - Add document parsing, embedding generation, and vector index creation (JSONL index).
3. **Answer generation**
   - Replace stub response with a Vertex AI (Gemini) model invocation (this project uses
     Gemini, not OpenAI).
4. **Deployment**
   - Add service layer (FastAPI/Cloud Run) and CI/CD workflows.

## Notes

- The current modules are scaffolding; connect them to your chosen data store and models.
- Update dependencies as needed once the detailed design is confirmed.
