import importlib.util
import unittest
from unittest.mock import patch


class ApiTests(unittest.TestCase):
    @unittest.skipIf(
        importlib.util.find_spec("fastapi") is None,
        "fastapi is not installed",
    )
    def test_healthz_requires_env(self) -> None:
        from fastapi.testclient import TestClient
        from rag_chatbot.api import app

        client = TestClient(app)
        with patch("rag_chatbot.api.AppConfig.from_env") as mock_config:
            mock_config.return_value.validate.return_value = ["GCP_PROJECT_ID"]
            response = client.get("/healthz")
        self.assertEqual(response.status_code, 500)

    @unittest.skipIf(
        importlib.util.find_spec("fastapi") is None,
        "fastapi is not installed",
    )
    def test_chat_returns_sources(self) -> None:
        from fastapi.testclient import TestClient
        from rag_chatbot.api import app

        client = TestClient(app)
        with patch("rag_chatbot.api.AppConfig.from_env") as mock_config, patch(
            "rag_chatbot.api.retrieve_context"
        ) as mock_retrieve, patch(
            "rag_chatbot.api.generate_answer"
        ) as mock_generate, patch(
            "rag_chatbot.api.initialize_vertex_ai"
        ):
            mock_config.return_value.validate.return_value = []
            mock_retrieve.return_value = []
            mock_generate.return_value.answer = "Hello"
            mock_generate.return_value.sources = []
            response = client.post("/chat", json={"query": "hi"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["answer"], "Hello")


if __name__ == "__main__":
    unittest.main()
