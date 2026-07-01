def profile_quality_score(
        candidate_features
):

    score = 1.0

    # Too few skills

    if candidate_features["num_skills"] < 3:

        score -= 0.2

    # Too many skills (possible stuffing)

    if candidate_features["num_skills"] > 40:

        score -= 0.3

    # Very low experience

    if (
        candidate_features[
            "years_experience"
        ] < 1

        and

        candidate_features[
            "num_skills"
        ] > 15
    ):

        score -= 0.3

    # Excessive job hopping

    num_companies = candidate_features[
        "num_companies"
    ]

    experience = max(
        candidate_features[
            "years_experience"
        ],
        1
    )

    jobs_per_year = (
        num_companies /
        experience
    )

    if jobs_per_year > 1.5:

        score -= 0.2

    # Low recruiter engagement

    if (
        candidate_features[
            "response_rate"
        ] < 0.1
    ):

        score -= 0.1

    # Missing education

    if len(
        candidate_features[
            "degrees"
        ]
    ) == 0:

        score -= 0.1

    return max(score, 0)