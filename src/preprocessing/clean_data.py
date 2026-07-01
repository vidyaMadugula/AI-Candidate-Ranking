def clean_candidate(candidate):

    # Ensure mandatory sections exist
    candidate.setdefault("profile", {})
    candidate.setdefault("career_history", [])
    candidate.setdefault("education", [])
    candidate.setdefault("skills", [])
    candidate.setdefault("certifications", [])
    candidate.setdefault("languages", [])
    candidate.setdefault("redrob_signals", {})

    profile = candidate["profile"]

    # Fill missing profile fields
    profile.setdefault("summary", "")
    profile.setdefault("headline", "")
    profile.setdefault("current_title", "")
    profile.setdefault("current_industry", "")
    profile.setdefault("years_of_experience", 0)

    return candidate