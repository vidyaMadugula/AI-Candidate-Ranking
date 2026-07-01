from datetime import datetime


def behavior_score(features):

    score = 0

    # ----------------------------------
    # Open to Work
    # ----------------------------------

    if features.get(
            "open_to_work", False):

        score += 1.0

    # ----------------------------------
    # Last Active Date
    # JD explicitly mentions this
    # ----------------------------------

    last_active = features.get(
        "last_active_date"
    )

    if last_active:

        try:

            days_inactive = (
                datetime.now() -
                datetime.strptime(
                    last_active,
                    "%Y-%m-%d"
                )
            ).days

            if days_inactive <= 14:
                score += 1.0

            elif days_inactive <= 60:
                score += 0.7

            elif days_inactive <= 120:
                score += 0.4

            elif days_inactive <= 180:
                score += 0.1

            else:
                # Candidate inactive for > 6 months
                score -= 0.3

        except ValueError:
            pass

    # ----------------------------------
    # Notice Period
    # ----------------------------------

    notice = features.get(
        "notice_period",
        180
    )

    if notice <= 30:
        score += 1.0

    elif notice <= 60:
        score += 0.8

    elif notice <= 90:
        score += 0.5

    elif notice <= 120:
        score += 0.2

    # ----------------------------------
    # Recruiter Response Rate
    # ----------------------------------

    response_rate = features.get(
        "response_rate",
        0
    )

    score += response_rate

    # Very poor response rate penalty

    if response_rate < 0.10:
        score -= 0.3

    # ----------------------------------
    # Average Response Time
    # ----------------------------------

    response_time = features.get(
        "avg_response_time_hours",
        999
    )

    if response_time <= 24:
        score += 0.5

    elif response_time <= 72:
        score += 0.3

    elif response_time <= 168:
        score += 0.1

    # ----------------------------------
    # Interview Completion
    # ----------------------------------

    score += features.get(
        "interview_completion",
        0
    )

    # ----------------------------------
    # GitHub Activity
    # ----------------------------------

    github = features.get(
        "github_score",
        -1
    )

    if github >= 8:
        score += 1.0

    elif github >= 5:
        score += 0.5

    elif github == -1:
        score += 0.2

    # ----------------------------------
    # Profile Completeness
    # ----------------------------------

    completeness = features.get(
        "profile_completeness",
        0
    )

    if completeness >= 90:
        score += 0.5

    elif completeness >= 75:
        score += 0.3

    # ----------------------------------
    # Profile Views
    # ----------------------------------

    views = features.get(
        "profile_views",
        0
    )

    if views >= 100:
        score += 0.8

    elif views >= 50:
        score += 0.4

    elif views >= 10:
        score += 0.2

    # ----------------------------------
    # Saved by Recruiters
    # ----------------------------------

    saved = features.get(
        "saved_by_recruiters",
        0
    )

    if saved >= 10:
        score += 0.8

    elif saved >= 5:
        score += 0.4

    elif saved >= 1:
        score += 0.2

    # ----------------------------------
    # Search Appearances
    # ----------------------------------

    appearances = features.get(
        "search_appearances",
        0
    )

    if appearances >= 250:
        score += 0.6

    elif appearances >= 100:
        score += 0.3

    # ----------------------------------
    # Connections
    # ----------------------------------

    connections = features.get(
        "connection_count",
        0
    )

    if connections >= 500:
        score += 0.3

    elif connections >= 100:
        score += 0.1

    # ----------------------------------
    # Offer Acceptance Rate
    # ----------------------------------

    offer_rate = features.get(
        "offer_acceptance_rate",
        -1
    )

    if offer_rate != -1:
        score += (
            offer_rate * 0.5
        )

    # ----------------------------------
    # Verified Contact Information
    # ----------------------------------

    if features.get(
            "verified_email", False):

        score += 0.2

    if features.get(
            "verified_phone", False):

        score += 0.2

    # ----------------------------------
    # LinkedIn Connected
    # ----------------------------------

    if features.get(
            "linkedin_connected",
            False):

        score += 0.2

    # ----------------------------------
    # Normalize
    # Maximum score ≈ 10.3
    # ----------------------------------

    return max(
        0.0,
        min(score / 10.3, 1.0)
    )