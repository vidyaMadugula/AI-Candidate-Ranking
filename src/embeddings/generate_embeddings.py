from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingGenerator:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            local_files_only=True
        )

    def encode(self, text):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding