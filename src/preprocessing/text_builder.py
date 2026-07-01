def build_profile_text(candidate):

    profile = candidate.get("profile", {})

    text_parts = []

    # Basic profile
    text_parts.append(
        f"Current Title: {profile.get('current_title', '')}"
    )

    text_parts.append(
        f"Headline: {profile.get('headline', '')}"
    )

    text_parts.append(
        f"Summary: {profile.get('summary', '')}"
    )

    text_parts.append(
        f"Industry: {profile.get('current_industry', '')}"
    )

    text_parts.append(
        f"Years Experience: {profile.get('years_of_experience', 0)}"
    )

    # Skills
    skills = candidate.get("skills", [])

    skill_text = ", ".join(
        skill["name"]
        for skill in skills
    )

    text_parts.append(
        f"Skills: {skill_text}"
    )

    # Career history
    for job in candidate.get("career_history", []):

        job_text = f"""
        Company: {job.get('company', '')}
        Title: {job.get('title', '')}
        Industry: {job.get('industry', '')}
        Description: {job.get('description', '')}
        """

        text_parts.append(job_text)

    # Education
    for edu in candidate.get("education", []):

        edu_text = f"""
        Degree: {edu.get('degree', '')}
        Field: {edu.get('field_of_study', '')}
        Institution: {edu.get('institution', '')}
        """

        text_parts.append(edu_text)

    return "\n".join(text_parts)