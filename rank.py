import pickle
from pathlib import Path
import argparse
import pandas as pd
from preprocess import preprocess_candidates
from build_index import build_faiss_index

from src.embeddings.generate_embeddings import (
    EmbeddingGenerator
)

from src.retrieval.retrieve import (
    CandidateRetriever
)

from src.retrieval.bm25_retriever import (
    BM25Retriever
)

from src.reranking.diversity_reranker import (
    DiversityReranker
)

from src.scoring.hybrid_scorer import (
    final_score
)

from src.scoring.career_fit import (
    career_fit_score
)

from src.explainability.explainer import (
    generate_explanation
)


project_root = Path(__file__).resolve().parent

JD_PRIORITY_SKILLS = [

    "rag",
    "langchain",
    "faiss",
    "semantic search",
    "information retrieval",
    "retrieval",
    "learning to rank",
    "recommendation systems",
    "recommendation engine",
    "bm25",
    "vector search",
    "vector database",
    "pinecone",
    "qdrant",
    "milvus",
    "weaviate",
    "embeddings",
    "embedding",
    "sentence transformers",
    "llm",
    "llms",
    "transformers",
    "pgvector",
    "opensearch",
    "elasticsearch",
    "haystack",
    "llamaindex",
    "python"
]


def generate_csv_reasoning(candidate):

    features = candidate.get(
        "candidate_features",
        {}
    )

    title = features.get(
        "current_title",
        "Candidate"
    )

    years = round(
        features.get(
            "years_experience",
            0
        ),
        1
    )

    candidate_skills = [

        skill.lower().strip()

        for skill in features.get(
            "skill_names",
            []
        )

    ]

    # --------------------------------------------------
    # Select skills most relevant to the job description
    # --------------------------------------------------

    matched_skills = []

    for skill in JD_PRIORITY_SKILLS:

        if skill in candidate_skills:
            matched_skills.append(skill)

    # Stop after collecting 4 relevant skills
        if len(matched_skills) == 4:
            break

    # Fill remaining slots with other profile skills

    if len(matched_skills) < 4:

        for skill in candidate_skills:

            if skill not in matched_skills:

                matched_skills.append(skill)

            if len(matched_skills) == 4:
                break
    # Format skills nicely
    if not matched_skills:
        skill_text = "relevant technical skills"
    elif len(matched_skills) == 1:
        skill_text = matched_skills[0]
    elif len(matched_skills) == 2:
        skill_text = (
            f"{matched_skills[0]} and "
            f"{matched_skills[1]}"
        )
    else:
        skill_text = (
             ", ".join(matched_skills[:-1])
             + f" and {matched_skills[-1]}"
        )

    response_rate = features.get(
        "response_rate",
        None
    )

    # --------------------------------------------------
    # Opening
    # --------------------------------------------------

    if years >= 8:

        opening = (
            f"{title} with {years} years of experience"
        )

    elif years >= 5:

        opening = (
            f"{title} with {years} years of industry experience"
        )

    else:

        opening = (
            f"{title} with {years} years of relevant experience"
        )

    # --------------------------------------------------
    # Middle
    # --------------------------------------------------

    middle = f"Demonstrates expertise in {skill_text}"
    if response_rate is not None:
        if response_rate >= 0.75:
            middle += (
                f" while maintaining excellent recruiter responsiveness "
                f"({response_rate:.2f})"
            )
        elif response_rate >= 0.50:
            middle += (
                f" with positive recruiter responsiveness "
                f"({response_rate:.2f})"
            )
        elif response_rate >= 0.30:
            middle += (
                f" and consistent recruiter responsiveness "
                f"({response_rate:.2f})"
            )

    # --------------------------------------------------
    # Ending
    # --------------------------------------------------

    if years >= 8:

        ending = (
            "making the profile suitable for senior AI roles."
        )

    elif years >= 5:

        ending = (
            "making the profile a strong match for the role."
        )

    else:

        ending = (
            "providing a solid foundation for the required responsibilities."
        )

    return f"{opening}. {middle}, {ending}"

class CandidateRanker:

    def __init__(
            self,
            data_dir="data/processed"
    ):

        self.embedder = EmbeddingGenerator()

        self.retriever = CandidateRetriever(data_dir)

        self.bm25 = BM25Retriever(data_dir)

        self.diversity = DiversityReranker()

        candidate_ids_path = (
            project_root /
            data_dir /
            "candidate_ids.pkl"
        )

        with open(
                candidate_ids_path,
                "rb"
        ) as f:

            self.candidate_ids = pickle.load(f)

        candidate_features_path = (
            project_root /
            data_dir /
            "candidate_features.pkl"
        )

        with open(
                candidate_features_path,
                "rb"
        ) as f:

            self.features = pickle.load(f)

    def rank(
            self,
            job_description,
            required_skills,
            mandatory_skills,
            min_experience=0,
            top_k=1000
    ):

        # ==========================================
        # Embed JD
        # ==========================================

        jd_embedding = self.embedder.encode(
            job_description
        )

        # ==========================================
        # Semantic Retrieval
        # ==========================================

        semantic_scores, semantic_indices = (

            self.retriever.retrieve(
                jd_embedding,
                top_k=top_k
            )

        )

        # ==========================================
        # BM25 Retrieval
        # ==========================================

        bm25_scores, bm25_indices = (

            self.bm25.retrieve(
                required_skills,
                top_k=top_k
            )

        )

        semantic_dict = dict(
            zip(
                semantic_indices,
                semantic_scores
            )
        )

        bm25_dict = dict(
            zip(
                bm25_indices,
                bm25_scores
            )
        )

        ranked_candidates = []

        # ==========================================
        # Candidate Pool
        # ==========================================

        all_indices = list(

            set(

                list(semantic_indices[:300])

                +

                list(bm25_indices[:300])

            )

        )

        # ==========================================
        # Candidate Scoring
        # ==========================================

        for idx in all_indices:

            idx = int(idx)
            if idx < 0 or idx >= len(self.features):
                continue
            feature = self.features[idx]

            # --------------------------------------
            # Remove obvious mismatches
            # --------------------------------------

            career_score = career_fit_score(
                feature
            )

            if career_score < 0.15:
                continue

            # --------------------------------------
            # Retrieval Scores
            # --------------------------------------

            semantic_score = float(

                semantic_dict.get(
                    idx,
                    0.0
                )

            )

            bm25_score = float(

                bm25_dict.get(
                    idx,
                    0.0
                )

            )

            bm25_score = min(
                bm25_score / 10,
                1.0
            )

            retrieval_score = (

                0.6 * semantic_score

                +

                0.4 * bm25_score

            )

            # --------------------------------------
            # Final Hybrid Score
            # --------------------------------------

            score_dict = final_score(

                retrieval_score,

                feature,

                required_skills,

                mandatory_skills,

                min_experience

            )

            # --------------------------------------
            # Generate Explanation
            # --------------------------------------

            explanation = generate_explanation(

                feature,

                {

                    "required_skills":
                        required_skills,

                    "mandatory_skills":
                        mandatory_skills,

                    "min_experience":
                        min_experience

                }

            )

            # --------------------------------------
            # Store Candidate
            # --------------------------------------

            ranked_candidates.append({

                "candidate_id":
                    self.candidate_ids[idx],

                "candidate_features":
                    feature,

                "final_score":
                    score_dict["final_score"],

                "retrieval_score":
                    retrieval_score,

                "semantic_score":
                    score_dict["semantic_score"],

                "skill_score":
                    score_dict["skill_score"],

                "experience_score":
                    score_dict["experience_score"],

                "behavior_score":
                    score_dict["behavior_score"],

                "career_fit_score":
                    score_dict["career_fit_score"],

                "profile_quality_score":
                    score_dict[
                        "profile_quality_score"
                    ],

                "skill_verification_score":
                    score_dict[
                        "skill_verification_score"
                    ],

                "mandatory_skill_penalty":
                    score_dict[
                        "mandatory_skill_penalty"
                    ],

                "honeypot_penalty":
                    score_dict[
                        "honeypot_penalty"
                    ],

                "explanation":
                    explanation

            })

        # ==========================================
        # Sort Candidates
        # ==========================================

        ranked_candidates = sorted(

            ranked_candidates,

            key=lambda x: x["final_score"],

            reverse=True

        )

        # ==========================================
        # Diversity Re-ranking
        # ==========================================

        ranked_candidates = (

            self.diversity.rerank(

                ranked_candidates,

                self.features,

                top_k

            )

        )

        return ranked_candidates[:100]


# ==========================================================
# Command Line Entry Point
# ==========================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(

        description=(
            "Rank candidates and generate "
            "submission CSV."
        )

    )

    parser.add_argument(

        "--candidates",

        required=True,

        help=(
            "Path to candidates JSONL file "
            "(kept for challenge compatibility)"
        )

    )

    parser.add_argument(

        "--out",

        required=True,

        help="Output submission CSV path"

    )

    args = parser.parse_args()

    # print(
    #     "\nLoading ranking system..."
    # )

    # ranker = CandidateRanker()
    print(
    "\nLoading ranking system..."
    )

    processed = Path("data/processed")

    required_files = [
        processed / "candidate_embeddings.npy",

        processed / "candidate_features.pkl",

        processed / "candidate_ids.pkl",

        processed / "skill_vocabulary.pkl",

        processed / "candidate_index.faiss"

    ]

    if not all(file.exists() for file in required_files):
        processed.mkdir(
            parents=True,
            exist_ok=True
        )

        print(
            "\nProcessed artifacts not found."
        )

        print(
            "Running preprocessing..."
        )

        preprocess_candidates(

            args.candidates,

            output_dir="data/processed"

        )

        print(
            "\nBuilding FAISS index..."
        )

        build_faiss_index(output_dir="data/processed")

        print(
            "\nPreprocessing completed."
        )

    ranker = CandidateRanker()

    job_description = """

    Senior AI Engineer with experience in
    Retrieval-Augmented Generation,
    semantic search, embeddings,
    vector databases, ranking systems,
    recommendation systems and Python.

    """

    required_skills = [

        "python",
        "rag",
        "faiss",
        "embeddings",
        "retrieval",
        "ranking",
        "semantic search",
        "langchain",
        "vector database"

    ]

    mandatory_skills = [

        "python",
        "rag"

    ]

    print(
        "\nRanking candidates..."
    )

    results = ranker.rank(

        job_description=job_description,

        required_skills=required_skills,

        mandatory_skills=mandatory_skills,

        min_experience=5,

        top_k=1000

    )

    print(
        "\nGenerating submission..."
    )

    rows = []

    for rank, candidate in enumerate(

            results[:100],

            start=1

    ):

        reasoning = generate_csv_reasoning(
            candidate
        )

        rows.append({

            "candidate_id":
                candidate[
                    "candidate_id"
                ],

            "rank":
                rank,

            "score":
                round(

                    candidate[
                        "final_score"
                    ],

                    6

                ),

            "reasoning":
                reasoning

        })

    submission = pd.DataFrame(
        rows
    )

    submission = submission.sort_values(
        by="rank"
    )

    if args.out.endswith(".xlsx"):
        submission.to_excel(
            args.out,
            index=False,
            engine="openpyxl"
        )
    else:
        submission.to_csv(
            args.out,
            index=False
        )

    print(

        f"\nSubmission saved to:\n"

        f"{args.out}"

    )

    print(

        "\nGenerated "

        f"{len(submission)} "

        "ranked candidates."

    )