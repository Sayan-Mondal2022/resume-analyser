from sentence_transformers import SentenceTransformer
from numpy import ndarray


class Embedder:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, text: str) -> ndarray:
        return self.model.encode(text)

    def encode_batch(self, texts: list[str]) -> list[ndarray]:
        return self.model.encode(texts)
