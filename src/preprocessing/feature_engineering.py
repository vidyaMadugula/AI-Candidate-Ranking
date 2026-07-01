from collections import Counter


def extract_features(candidate):

    profile = candidate["profile"]

    features = {}

    # ====================================================
    # Basic Profile Features
    # ====================================================

    features["candidate_id"] = candidate[
        "candidate_id"
    ]

    features["current_title"] = profile.get(
        "current_title",
        ""
    )

    features["industry"] = profile.get(
        "current_industry",
        ""
    )

    features["location"] = profile.get(
        "location",
        ""
    )

    features["country"] = profile.get(
        "country",
        ""
    )

    features["years_experience"] = profile.get(
        "years_of_experience",
        0
    )

    # ====================================================
    # Skills Features
    # ====================================================

    skills = candidate.get(
        "skills",
        []
    )

    features["skill_names"] = [

        skill.get(
            "name",
            ""
        ).lower()

        for skill in skills

    ]

    features["num_skills"] = len(
        skills
    )

    # Skill durations (for honeypot detection)

    features["skill_durations"] = [

        skill.get(
            "duration_months",
            0
        )

        for skill in skills

    ]

    # Count expert skills

    features["expert_skills"] = sum(

        1

        for skill in skills

        if skill.get(
            "proficiency",
            ""
        ).lower() == "expert"

    )

    # ====================================================
    # Career History Features
    # ====================================================

    career = candidate.get(
        "career_history",
        []
    )

    features["companies"] = [

        job.get(
            "company",
            ""
        )

        for job in career

    ]

    features["job_titles"] = [

        job.get(
            "title",
            ""
        )

        for job in career

    ]

    features["career_descriptions"] = [

        job.get(
            "description",
            ""
        )

        for job in career

    ]

    features["career_durations"] = [

        job.get(
            "duration_months",
            0
        )

        for job in career

    ]

    features["num_companies"] = len(
        career
    )

    features["industries_worked"] = list(

        set(

            job.get(
                "industry",
                ""
            )

            for job in career

            if job.get(
                "industry"
            )

        )

    )

    # ====================================================
    # Education Features
    # ====================================================

    education = candidate.get(
        "education",
        []
    )

    features["degrees"] = [

        edu.get(
            "degree",
            ""
        )

        for edu in education

    ]

    # ====================================================
    # Certification Features
    # ====================================================

    certifications = candidate.get(
        "certifications",
        []
    )

    features["num_certifications"] = len(
        certifications
    )

    # ====================================================
    # Behavioral Signals
    # ====================================================

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    features["open_to_work"] = signals.get(
        "open_to_work_flag",
        False
    )

    features["willing_to_relocate"] = signals.get(
        "willing_to_relocate",
        False
    )

    features["notice_period"] = signals.get(
        "notice_period_days",
        180
    )

    features["profile_completeness"] = signals.get(
        "profile_completeness_score",
        0
    )

    features["last_active_date"] = signals.get(
        "last_active_date",
        None
    )

    features["response_rate"] = signals.get(
        "recruiter_response_rate",
        0
    )

    features["avg_response_time_hours"] = signals.get(
        "avg_response_time_hours",
        999
    )

    features["connection_count"] = signals.get(
        "connection_count",
        0
    )

    features["endorsements_received"] = signals.get(
        "endorsements_received",
        0
    )

    features["skill_assessment_scores"] = signals.get(
        "skill_assessment_scores",
        {}
    )

    features["github_score"] = signals.get(
        "github_activity_score",
        -1
    )

    features["profile_views"] = signals.get(
        "profile_views_received_30d",
        0
    )

    features["saved_by_recruiters"] = signals.get(
        "saved_by_recruiters_30d",
        0
    )

    features["search_appearances"] = signals.get(
        "search_appearance_30d",
        0
    )

    features["interview_completion"] = signals.get(
        "interview_completion_rate",
        0
    )

    features["offer_acceptance_rate"] = signals.get(
        "offer_acceptance_rate",
        -1
    )

    features["verified_email"] = signals.get(
        "verified_email",
        False
    )

    features["verified_phone"] = signals.get(
        "verified_phone",
        False
    )

    features["linkedin_connected"] = signals.get(
        "linkedin_connected",
        False
    )

    return features