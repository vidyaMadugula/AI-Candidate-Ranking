AI_SKILLS = {

    "faiss",
    "pinecone",
    "qdrant",
    "milvus",
    "weaviate",
    "rag",
    "langchain",
    "embeddings",
    "embedding",
    "llm",
    "lora",
    "qlora",
    "retrieval",
    "semantic search",
    "vector database"

}

BAD_TITLES = {

    "marketing manager",
    "operations manager",
    "customer support",
    "graphic designer",
    "seo specialist",
    "sales manager",
    "brand manager",
    "content writer"

}

PRODUCTION_EVIDENCE = {

    "retrieval",
    "ranking",
    "search",
    "recommendation",
    "embedding",
    "embeddings",
    "rag",
    "pipeline",
    "production",
    "evaluation",
    "deployed",
    "faiss",
    "pinecone"

}


class HoneypotDetector:

    def detect(
            self,
            candidate_features
    ):

        penalty = 1.0

        years_exp = candidate_features.get(
            "years_experience",
            0
        )

        total_exp_months = (
            years_exp * 12
        )

        num_skills = candidate_features.get(
            "num_skills",
            0
        )

        current_title = (
            candidate_features.get(
                "current_title",
                ""
            ).lower()
        )

        skill_durations = (
            candidate_features.get(
                "skill_durations",
                []
            )
        )

        expert_skills = (
            candidate_features.get(
                "expert_skills",
                0
            )
        )

        candidate_skills = set(

            candidate_features.get(
                "skill_names",
                []
            )

        )

        claimed_ai_skills = (

            candidate_skills.intersection(
                AI_SKILLS
            )

        )

        # ==========================================
        # Senior title with low experience
        # ==========================================

        senior_titles = [

            "senior",
            "lead",
            "principal",
            "architect",
            "staff"

        ]

        if any(

                title in current_title

                for title in senior_titles

        ):

            if years_exp < 3:

                penalty *= 0.1

                print(
                    "Senior title anomaly triggered"
                )

        # ==========================================
        # Title-Skill Incoherence
        # ==========================================

        if (

                current_title in BAD_TITLES

                and

                len(claimed_ai_skills) >= 3

        ):

            penalty *= 0.2

            print(
                "Title-skill mismatch triggered"
            )

        # ==========================================
        # AI Skills Without Career Evidence
        # ==========================================

        career_text = " ".join(

            candidate_features.get(
                "career_descriptions",
                []
            )

        ).lower()

        evidence_found = any(

            keyword in career_text

            for keyword in PRODUCTION_EVIDENCE

        )

        if (

                len(claimed_ai_skills) >= 5

                and

                not evidence_found

        ):

            penalty *= 0.3

            print(
                "No career evidence anomaly triggered"
            )

        # ==========================================
        # Too many expert skills
        # ==========================================

        if expert_skills > 8:

            if years_exp < 5:

                penalty *= 0.5

                print(
                    "Expert skills anomaly triggered"
                )

            if skill_durations:

                zero_duration_skills = sum(

                    1

                    for duration in skill_durations

                    if duration <= 1

                )

                if zero_duration_skills >= 5:

                    penalty *= 0.4

                    print(
                        "Expert skills without usage anomaly"
                    )

        # ==========================================
        # Skill Duration Validation
        # ==========================================

        if skill_durations:

            total_skill_duration = sum(
                skill_durations
            )

            if (

                    total_skill_duration >

                    total_exp_months * 6

            ):

                penalty *= 0.7

                print(
                    "Skill duration anomaly triggered"
                )

            for duration in skill_durations:

                if (

                        duration >

                        total_exp_months * 1.5

                ):

                    penalty *= 0.8

                    print(
                        "Individual skill duration anomaly"
                    )

                    break

        # ==========================================
        # Skill stuffing
        # ==========================================

        if (

                years_exp < 2

                and

                num_skills > 40

        ):

            penalty *= 0.7

            print(
                "Skill stuffing anomaly triggered"
            )

        # ==========================================
        # Too many companies for low experience
        # ==========================================

        num_companies = candidate_features.get(
            "num_companies",
            0
        )

        if (

                years_exp < 2

                and

                num_companies > 5

        ):

            penalty *= 0.3

            print(
                "Company hopping anomaly triggered"
            )

        # ==========================================
        # Timeline Validation
        # ==========================================

        career_durations = candidate_features.get(
            "career_durations",
            []
        )

        if career_durations:

            total_career_months = sum(
                career_durations
            )

            if (

                    total_career_months >

                    total_exp_months * 2

            ):

                penalty *= 0.7

                print(
                    "Career duration mismatch triggered"
                )

            elif (

                    total_exp_months >

                    total_career_months * 2

            ):

                penalty *= 0.7

                print(
                    "Experience mismatch triggered"
                )

        # ==========================================
        # Impossible values
        # ==========================================

        if years_exp > 50:

            penalty *= 0.1

        if years_exp < 0:

            penalty = 0.0

        # ==========================================
        # Final Range
        # ==========================================

        penalty = max(
            0.0,
            min(
                penalty,
                1.0
            )
        )

        return penalty