def skill_verification_score(
        candidate_features
):

    score = 0.5

    # ====================================
    # Skill Assessment Scores
    # ====================================

    assessment_scores = candidate_features.get(
        "skill_assessment_scores",
        {}
    )

    if assessment_scores:

        avg_score = (

            sum(
                assessment_scores.values()
            )

            /

            len(
                assessment_scores
            )

        )

        # Strong evidence of real skill

        if avg_score >= 75:

            score += 0.30

        elif avg_score >= 60:

            score += 0.20

        elif avg_score >= 40:

            score += 0.10

        else:

            score -= 0.20

    # ====================================
    # Endorsements
    # ====================================

    endorsements = candidate_features.get(
        "endorsements_received",
        0
    )

    if endorsements >= 50:

        score += 0.20

    elif endorsements >= 20:

        score += 0.10

    elif endorsements == 0:

        score -= 0.05

    # ====================================
    # LinkedIn Connected
    # ====================================

    if candidate_features.get(
            "linkedin_connected",
            False):

        score += 0.05

    # ====================================
    # Expert Skill Stuffing Detection
    # ====================================

    expert_skills = candidate_features.get(
        "expert_skills",
        0
    )

    years_exp = candidate_features.get(
        "years_experience",
        0
    )

    if (

            expert_skills > 10

            and

            years_exp < 5

    ):

        score -= 0.20

    career_text = " ".join(
        candidate_features.get(
            "career_descriptions",
            []
        )
    ).lower()
    ai_evidence = {
        "retrieval",
        "ranking",
        "recommendation",
        "search",
        "rag",
        "embedding",
        "llm",
        "faiss",
        "vector search"
    }
    evidence_count = sum(
        1
        for word in ai_evidence
        if word in career_text
    )

# Strong AI claims without evidence
    if expert_skills >= 8 and evidence_count == 0:
        score -= 0.20
    
    
    
    # ====================================
    # Normalize
    # ====================================

    return max(
        0.0,
        min(score, 1.0)
    )