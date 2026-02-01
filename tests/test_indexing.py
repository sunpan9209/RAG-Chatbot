import importlib.util
import unittest
from pathlib import Path

from rag_chatbot.embeddings import chunk_text
from rag_chatbot.indexing import IndexEntry, VectorIndex


class IndexingTests(unittest.TestCase):
    def test_chunk_text(self) -> None:
        chunks = list(chunk_text("abcd", chunk_size=2))
        self.assertEqual(chunks, ["ab", "cd"])

    @unittest.skipIf(
        importlib.util.find_spec("vertexai") is None,
        "vertexai is not installed",
    )
    def test_vector_index_roundtrip(self) -> None:
        tmp_path = Path("tests/tmp_index.jsonl")
        entries = [
            IndexEntry(uri="file#0", content="hello", embedding=[0.1, 0.2]),
            IndexEntry(uri="file#1", content="world", embedding=[0.3, 0.4]),
        ]
        index = VectorIndex(entries=entries)
        index.save(tmp_path)

        reloaded = VectorIndex.load(tmp_path)
        tmp_path.unlink()

        self.assertEqual(len(reloaded.entries), 2)
        self.assertEqual(reloaded.entries[0].uri, "file#0")
        self.assertEqual(reloaded.entries[1].content, "world")
        self.assertEqual(reloaded.entries[1].embedding, [0.3, 0.4])


if __name__ == "__main__":
    unittest.main()
