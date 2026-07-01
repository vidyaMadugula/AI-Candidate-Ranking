class DataValidator:

    def validate(
            self,
            candidate_features
    ):

        issues = []

        # Missing education

        if len(
                candidate_features.get(
                    "degrees", []
                )
        ) == 0:

            issues.append(
                "Missing education information"
            )

        # Missing skills

        if candidate_features.get(
                "num_skills", 0) == 0:

            issues.append(
                "No skills listed"
            )

        # Skill stuffing

        if candidate_features.get(
                "num_skills", 0) > 40:

            issues.append(
                "Possible skill stuffing detected"
            )

        # Too many skills for very low experience

        years_exp = candidate_features.get(
            "years_experience", 0
        )

        num_skills = candidate_features.get(
            "num_skills", 0
        )

        if (
                years_exp < 1
                and
                num_skills > 15
        ):

            issues.append(
                "Unusually high number of skills "
                "for experience level"
            )

        # Excessive job hopping

        num_companies = candidate_features.get(
            "num_companies", 0
        )

        if years_exp > 0:

            jobs_per_year = (
                    num_companies /
                    years_exp
            )

            if jobs_per_year > 1.5:

                issues.append(
                    "Possible excessive job hopping"
                )

        # Invalid experience

        if years_exp < 0:

            issues.append(
                "Invalid experience value"
            )

        # Very low recruiter engagement

        response_rate = candidate_features.get(
            "response_rate", 0
        )

        if response_rate < 0.05:

            issues.append(
                "Very low recruiter response rate"
            )

        # Missing company history

        if candidate_features.get(
                "num_companies", 0) == 0:

            issues.append(
                "No work history available"
            )

        # GitHub anomaly

        github_score = candidate_features.get(
            "github_score", -1
        )

        if (
                github_score > 9
                and
                years_exp < 1
        ):

            issues.append(
                "Unusually high GitHub activity "
                "for experience level"
            )

        return issues