from src.scoring.behavior_scorer import (
    behavior_score
)

from src.scoring.profile_quality import (
    profile_quality_score
)

from src.validation.honeypot_detector import (
    HoneypotDetector
)

from src.scoring.career_fit import (
    career_fit_score
)

from src.scoring.skill_verification import (
    skill_verification_score
)


# ====================================================
# Tunable Weights
# ====================================================

SEMANTIC_WEIGHT = 0.25
SKILL_WEIGHT = 0.20
EXPERIENCE_WEIGHT = 0.05
BEHAVIOR_WEIGHT = 0.05
QUALITY_WEIGHT = 0.05
CAREER_WEIGHT = 0.35
SKILL_VERIFICATION_WEIGHT = 0.05


def skill_match_score(
        candidate_features,
        required_skills
):

    candidate_skills = set(
        skill.lower()
        for skill in
        candidate_features["skill_names"]
    )

    skill_weights = {

        # Critical signals
        "rag": 4,
        "retrieval": 4,
        "embeddings": 4,
        "semantic search": 4,
        "faiss": 4,
        "pinecone": 4,
        "qdrant": 4,
        "milvus": 4,
        "weaviate": 4,
        "elasticsearch": 4,
        "opensearch": 4,

        # Very important
        "ranking": 3,
        "recommendation": 3,
        "langchain": 3,
        "sentence transformers": 3,

        # Nice to have
        "lora": 2,
        "qlora": 2,
        "peft": 2,
        "fine tuning": 2,

        # Basic requirement
        "python": 1
    }

    total_weight = sum(
        skill_weights.values()
    )

    matched_weight = 0

    for skill, weight in skill_weights.items():

        if any(
            skill in cand_skill
            or cand_skill in skill
            for cand_skill in candidate_skills
        ):
            matched_weight += weight
    return matched_weight / total_weight


def experience_match_score(
        candidate_features,
        min_experience
):

    candidate_exp = candidate_features[
        "years_experience"
    ]

    if min_experience == 0:
        return 1.0

    if candidate_exp >= min_experience:
        return 1.0

    return candidate_exp / min_experience


def mandatory_skill_penalty(
        candidate_features,
        mandatory_skills
):

    candidate_skills = set(
        skill.lower()
        for skill in candidate_features["skill_names"]
    )

    mandatory_skills = set(
        skill.lower()
        for skill in mandatory_skills
    )

    if len(mandatory_skills) == 0:
        return 1.0

    missing_skills = (
        mandatory_skills - candidate_skills
    )

    missing_ratio = (
        len(missing_skills)
        / len(mandatory_skills)
    )

    # Missing half or more mandatory skills

    if missing_ratio >= 0.5:
        return 0.1

    # Missing some mandatory skills

    elif missing_ratio > 0:
        return 0.5

    return 1.0


def final_score(
        semantic_score,
        candidate_features,
        required_skills,
        mandatory_skills,
        min_experience
):

    # ==================================
    # Individual Scores
    # ==================================

    skill_score = skill_match_score(
        candidate_features,
        required_skills
    )

    exp_score = experience_match_score(
        candidate_features,
        min_experience
    )

    behavior = behavior_score(
        candidate_features
    )

    quality = profile_quality_score(
        candidate_features
    )

    career = career_fit_score(
        candidate_features
    )

    skill_verification = (
        skill_verification_score(
            candidate_features
        )
    )

    # ==================================
    # Penalties
    # ==================================

    mandatory_penalty = (
        mandatory_skill_penalty(
            candidate_features,
            mandatory_skills
        )
    )

    detector = HoneypotDetector()

    honeypot_penalty = detector.detect(
        candidate_features
    )

    # ==================================
    # Final Score
    # ==================================

    score = (

        SEMANTIC_WEIGHT *
        semantic_score +

        SKILL_WEIGHT *
        skill_score +

        EXPERIENCE_WEIGHT *
        exp_score +

        BEHAVIOR_WEIGHT *
        behavior +

        QUALITY_WEIGHT *
        quality +

        CAREER_WEIGHT *
        career +

        SKILL_VERIFICATION_WEIGHT *
        skill_verification

    )

    # ==================================
    # Apply Penalties
    # ==================================

    score *= mandatory_penalty

    score *= honeypot_penalty

    # Keep score in range

    score = max(
        0.0,
        min(score, 1.0)
    )

    # ==================================
    # Return
    # ==================================

    return {

        "final_score":
            score,

        "semantic_score":
            semantic_score,

        "skill_score":
            skill_score,

        "experience_score":
            exp_score,

        "behavior_score":
            behavior,

        "profile_quality_score":
            quality,

        "career_fit_score":
            career,

        "skill_verification_score":
            skill_verification,

        "mandatory_skill_penalty":
            mandatory_penalty,

        "honeypot_penalty":
            honeypot_penalty
    }