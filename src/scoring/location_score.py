PREFERRED_CITIES = {

    "pune",
    "noida"

}

TIER1_CITIES = {

    "hyderabad",
    "mumbai",
    "delhi",
    "gurgaon",
    "bangalore",
    "chennai",
    "noida",
    "pune"

}


def location_score(candidate_features):

    score = 0.5

    location = candidate_features.get(
        "location",
        ""
    ).lower()

    willing_to_relocate = (
        candidate_features.get(
            "willing_to_relocate",
            False
        )
    )

    country = candidate_features.get(
        "country",
        ""
    ).lower()

    # Preferred locations

    if any(
            city in location
            for city in PREFERRED_CITIES
    ):

        score += 0.5

    # Tier-1 Indian cities

    elif any(
            city in location
            for city in TIER1_CITIES
    ):

        score += 0.3

    # Outside India

    elif country != "india":

        score -= 0.1

    # Relocation willingness

    if willing_to_relocate:

        score += 0.2

    return min(
        max(score, 0.0),
        1.0
    )