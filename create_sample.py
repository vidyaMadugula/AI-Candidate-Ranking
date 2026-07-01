import json
import random

good_titles = {
    "AI Engineer",
    "ML Engineer",
    "Data Scientist",
    "Data Engineer",
    "NLP Engineer",
    "Software Engineer",
    "Backend Engineer"
}

good = []
others = []

with open(
        "data/raw/candidates.jsonl",
        "r",
        encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        title = candidate["profile"][
            "current_title"
        ]

        if title in good_titles:
            good.append(line)
        else:
            others.append(line)

# Shuffle remaining candidates
random.shuffle(others)

# Keep more good profiles
selected = good[:60] + others[:60]

# Ensure exactly 130 candidates
selected = selected[:120]

with open(
        "data/demo_candidates.jsonl",
        "w",
        encoding="utf-8"
) as f:

    f.writelines(selected)

print(
    f"Saved {len(selected)} demo candidates"
)