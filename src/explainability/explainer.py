def generate_explanation(
        candidate_features,
        jd
):

    explanations = []

    # ====================================================
    # Skills Analysis
    # ====================================================

    candidate_skills = set(
        skill.lower()
        for skill in
        candidate_features.get(
            "skill_names",
            []
        )
    )

    required_skills = set(
        skill.lower()
        for skill in
        jd.get(
            "required_skills",
            []
        )
    )

    mandatory_skills = set(
        skill.lower()
        for skill in
        jd.get(
            "mandatory_skills",
            []
        )
    )

    negative_keywords = set(
        skill.lower()
        for skill in
        jd.get(
            "negative_keywords",
            []
        )
    )

    matched_skills = list(
        candidate_skills.intersection(
            required_skills
        )
    )

    missing_mandatory = list(
        mandatory_skills -
        candidate_skills
    )

    negative_matches = list(
        candidate_skills.intersection(
            negative_keywords
        )
    )

    # ====================================================
    # Skill Match
    # ====================================================

    if matched_skills:

        explanations.append(

            "Demonstrates strong alignment with the role through expertise in "

            + ", ".join(
                matched_skills[:5]
            )

        )

    else:

        explanations.append(

            "Limited direct overlap with the core technical requirements of the role"

        )

    # ====================================================
    # Missing Mandatory Skills
    # ====================================================

    if missing_mandatory:

        explanations.append(

            "Missing mandatory requirements such as "

            + ", ".join(
                missing_mandatory[:5]
            )

        )

    # ====================================================
    # Negative Indicators
    # ====================================================

    if negative_matches:

        explanations.append(

            "Profile contains potentially irrelevant skills including "

            + ", ".join(
                negative_matches
            )

        )

    # ====================================================
    # Experience
    # ====================================================

    candidate_exp = candidate_features.get(
        "years_experience",
        0
    )

    required_exp = jd.get(
        "min_experience",
        0
    )

    if candidate_exp >= required_exp:

        explanations.append(

            f"Exceeds the experience requirement with {candidate_exp:.1f} years of industry experience"

        )

    else:

        explanations.append(

            f"Has {candidate_exp:.1f} years of experience, which is below the preferred range for this role"

        )

    # ====================================================
    # Career Evidence
    # ====================================================

    career_text = " ".join(

        candidate_features.get(
            "career_descriptions",
            []

        )

    ).lower()

    evidence_words = [

        "retrieval",
        "ranking",
        "search",
        "recommendation",
        "embedding",
        "embeddings",
        "rag",
        "production",
        "pipeline",
        "evaluation",
        "deployed",
        "faiss",
        "pinecone"

    ]

    matched_evidence = [

        word

        for word in evidence_words

        if word in career_text

    ]

    if len(matched_evidence) >= 3:

        explanations.append(

            "Strong evidence of production AI experience through work involving "

            + ", ".join(
                matched_evidence[:4]
            )

        )

    elif matched_evidence:

        explanations.append(

            "Shows exposure to production AI systems through "

            + ", ".join(
                matched_evidence[:3]
            )

        )

    # ====================================================
    # Title-Skill Inconsistency
    # ====================================================

    suspicious_titles = {

        "marketing manager",
        "operations manager",
        "sales manager",
        "brand manager",
        "graphic designer",
        "content writer"

    }

    ai_skills = {

        "faiss",
        "pinecone",
        "rag",
        "langchain",
        "llm"

    }

    current_title = candidate_features.get(
        "current_title",
        ""
    ).lower()

    if (

        current_title in suspicious_titles

        and

        len(
            candidate_skills.intersection(
                ai_skills
            )
        ) >= 3

    ):

        explanations.append(

            "Profile shows some inconsistency between stated role and claimed AI expertise"

        )

    # ====================================================
    # Behavioral Signals
    # ====================================================

    if candidate_features.get(
            "open_to_work",
            False):

        explanations.append(

            "Actively open to new opportunities, improving recruiter engagement likelihood"

        )

    notice = candidate_features.get(
        "notice_period",
        180
    )

    if notice <= 30:

        explanations.append(

            "Can potentially join quickly due to a short notice period"

        )

    elif notice <= 60:

        explanations.append(

            "Has a moderate notice period that remains acceptable for hiring"

        )

    elif notice > 90:

        explanations.append(

            f"Longer notice period ({notice} days) may delay onboarding"

        )

    response_rate = candidate_features.get(
        "response_rate",
        0
    )

    if response_rate >= 0.7:

        explanations.append(

            "Shows strong recruiter engagement based on historical response behavior"

        )

    github = candidate_features.get(
        "github_score",
        -1
    )

    if github >= 7:

        explanations.append(

            "Demonstrates strong engineering engagement through GitHub activity"

        )

    # ====================================================
    # Profile Quality
    # ====================================================

    if candidate_features.get(
            "profile_completeness",
            0) >= 80:

        explanations.append(

            "Maintains a highly complete professional profile"

        )

    endorsements = candidate_features.get(
        "endorsements_received",
        0
    )

    if endorsements >= 20:

        explanations.append(

            "Has received strong peer endorsements, indicating professional credibility"

        )

    if candidate_features.get(
            "linkedin_connected",
            False):

        explanations.append(

            "Profile includes verified professional networking information"

        )

    # ====================================================
    # Relocation
    # ====================================================

    if candidate_features.get(
            "willing_to_relocate",
            False):

        explanations.append(

            "Open to relocation, increasing hiring flexibility"

        )

    # ====================================================
    # Positive explanations first
    # ====================================================

    positive_explanations = []
    negative_explanations = []

    negative_words = {

        "missing",
        "below",
        "limited",
        "delay",
        "inconsistency",
        "irrelevant"

    }

    for exp in explanations:

        if any(
                word in exp.lower()
                for word in negative_words
        ):

            negative_explanations.append(
                exp
            )

        else:

            positive_explanations.append(
                exp
            )

    final_explanations = (

        positive_explanations +

        negative_explanations

    )

    # ====================================================
    # Return top explanations
    # ====================================================

    return final_explanations[:6]