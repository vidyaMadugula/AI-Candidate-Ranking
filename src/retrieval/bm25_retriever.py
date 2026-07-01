import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi


project_root = Path(__file__).resolve().parents[2]


class BM25Retriever:

    def __init__(self,data_dir="data/processed"):

        features_path = (
            project_root /
            data_dir /
            "candidate_features.pkl"
        )

        with open(features_path, "rb") as f:

            self.features = pickle.load(f)

        corpus = []

        for candidate in self.features:

            text = " ".join(
                candidate["skill_names"]
            )

            corpus.append(
                text.split()
            )

        self.bm25 = BM25Okapi(corpus)

    def retrieve(
            self,
            query_skills,
            top_k=10
    ):

        tokenized_query = [

            skill.lower()

            for skill in query_skills
        ]

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(

            range(len(scores)),

            key=lambda i: scores[i],

            reverse=True

        )[:top_k]

        ranked_scores = [

            scores[idx]

            for idx in ranked_indices
        ]

        return ranked_scores, ranked_indices