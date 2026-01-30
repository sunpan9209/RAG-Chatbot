import unittest
from unittest.mock import MagicMock, patch

from rag_chatbot.chat import build_prompt, generate_answer
from rag_chatbot.config import AppConfig
from rag_chatbot.retrieval import RetrievedChunk


class ChatTests(unittest.TestCase):
    def test_build_prompt_includes_context(self) -> None:
        chunks = [RetrievedChunk(uri="file.txt", content="Hello", score=1.0)]
        prompt = build_prompt("Question?", chunks)
        self.assertIn("Hello", prompt)
        self.assertIn("Question?", prompt)

    @patch("rag_chatbot.chat.initialize_vertex_ai")
    @patch("rag_chatbot.chat.GenerativeModel")
    def test_generate_answer_calls_gemini(self, mock_model, mock_init) -> None:
        mock_instance = mock_model.return_value
        mock_instance.generate_content.return_value = MagicMock(text="Answer")
        config = AppConfig(
            gcp_project_id="project",
            gcp_region="us-central1",
            embedding_model="textembedding-gecko@latest",
            chat_model="gemini-1.5-pro",
            document_bucket="bucket",
            vector_index_path="index.jsonl",
        )
        chunks = [RetrievedChunk(uri="file.txt", content="Hello", score=1.0)]

        response = generate_answer(config, "Question?", chunks)

        mock_init.assert_called_once_with(config)
        mock_model.assert_called_once_with("gemini-1.5-pro")
        mock_instance.generate_content.assert_called_once()
        self.assertEqual(response.answer, "Answer")


if __name__ == "__main__":
    unittest.main()
