import faiss
import numpy as np
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]


class CandidateRetriever:

    def __init__(self,data_dir="data/processed"):

        index_path = (
            project_root /
            data_dir /
            "candidate_index.faiss"
        )

        self.index = faiss.read_index(
            str(index_path)
        )

    def retrieve(
            self,
            query_embedding,
            top_k=1000
    ):

        query_embedding = np.array(
            [query_embedding]
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        return scores[0], indices[0]