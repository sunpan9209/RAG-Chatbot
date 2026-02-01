import importlib.util
import os
import unittest
from unittest.mock import patch

if importlib.util.find_spec("fastapi") is None:
    raise unittest.SkipTest("fastapi is not installed")

from fastapi.testclient import TestClient

from rag_chatbot.api import app
from rag_chatbot.retrieval import RetrievedChunk


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_env = os.environ.copy()
        os.environ["GCP_PROJECT_ID"] = "project"
        os.environ["DOCUMENT_BUCKET"] = "bucket"

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_healthz_ok(self) -> None:
        client = TestClient(app)
        response = client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("rag_chatbot.api.generate_answer")
    @patch("rag_chatbot.api.retrieve_context")
    def test_chat_endpoint(self, mock_retrieve, mock_generate) -> None:
        mock_retrieve.return_value = [
            RetrievedChunk(uri="doc.txt", content="Hello", score=0.9)
        ]
        mock_generate.return_value = type(
            "Response",
            (),
            {"answer": "Hi there", "sources": mock_retrieve.return_value},
        )()
        client = TestClient(app)

        response = client.post("/chat", json={"query": "Hello?"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["answer"], "Hi there")
        self.assertEqual(payload["sources"][0]["uri"], "doc.txt")


if __name__ == "__main__":
    unittest.main()
