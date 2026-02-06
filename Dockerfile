FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md /app/
COPY rag_chatbot /app/rag_chatbot

RUN pip install --no-cache-dir .

ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn rag_chatbot.api:app --host 0.0.0.0 --port ${PORT}"]
