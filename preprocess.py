import json
import pickle
import numpy as np
from tqdm import tqdm

from src.preprocessing.feature_engineering import extract_features
from src.preprocessing.text_builder import build_profile_text
from src.embeddings.generate_embeddings import EmbeddingGenerator


def preprocess_candidates(input_file, output_dir="data/processed", max_candidates=None):

    embedder = EmbeddingGenerator()

    candidate_ids = []
    embeddings = []
    features = []

    # Dynamic skill vocabulary
    all_skills = set()

    with open(input_file, "r", encoding="utf-8") as f:

        for idx, line in enumerate(tqdm(f)):

            candidate = json.loads(line)

            # Save candidate id
            candidate_ids.append(
                candidate["candidate_id"]
            )

            # Build dynamic skill vocabulary
            for skill in candidate.get("skills", []):

                skill_name = (
                    skill.get("name", "")
                    .lower()
                    .strip()
                )

                if skill_name:
                    all_skills.add(skill_name)

            # Build profile text
            profile_text = build_profile_text(
                candidate
            )

            # Create embedding
            embedding = embedder.encode(
                profile_text
            )

            embeddings.append(embedding)

            # Extract structured features
            candidate_features = extract_features(
                candidate
            )

            features.append(
                candidate_features
            )

            if (
                max_candidates and
                idx + 1 >= max_candidates
            ):
                break

    embeddings = np.array(embeddings,dtype=np.float32)

    # Save embeddings
    np.save(
        f"{output_dir}/candidate_embeddings.npy",
        embeddings
    )

    # Save candidate ids
    with open(
        f"{output_dir}/candidate_ids.pkl",
        "wb"
    ) as f:

        pickle.dump(candidate_ids, f)

    # Save candidate features
    with open(
        f"{output_dir}/candidate_features.pkl",
        "wb"
    ) as f:

        pickle.dump(features, f)

    # Save skill vocabulary
    with open(
        f"{output_dir}/skill_vocabulary.pkl",
        "wb"
    ) as f:

        pickle.dump(
            sorted(all_skills),
            f
        )

    print(
        f"Saved {len(all_skills)} unique skills"
    )

    print(
        f"Processed {len(candidate_ids)} candidates"
    )
    print("Saved Successfully")


if __name__ == "__main__":

    preprocess_candidates(
        "data/raw/candidates.jsonl",
    )