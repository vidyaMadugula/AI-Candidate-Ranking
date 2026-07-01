# ==========================================================
# CAREER FIT SCORER
# ==========================================================

# Small high-signal evidence vocabulary

PRODUCTION_EVIDENCE = {

    "retrieval",
    "ranking",
    "search",
    "recommendation",

    "embedding",
    "embeddings",
    "rag",
    "llm",

    "production",
    "deployed",
    "pipeline",

    "evaluation",
    "ndcg",
    "mrr",

    "faiss",
    "vector search"
}


HIGH_SIGNAL_TERMS = {

    "re-ranking",
    "reranking",
    "dense retrieval",
    "sparse retrieval",
    "vector database",
    "vector db",
    "candidate retrieval",
    "recommendation engine",
    "recommendation system",
    "personalization",
    "feature store",
    "online serving",
    "offline evaluation",
    "a/b testing",
    "ab testing",
    "search relevance",
    "relevance tuning",
    "click through rate",
    "ctr",
    "learning to rank",
    "ltr",
    "semantic retrieval"
}


CONSULTING_COMPANIES = {

    "tcs",
    "infosys",
    "wipro",
    "accenture",
    "cognizant",
    "capgemini",
    "mindtree",
    "hcl",
    "tech mahindra",
    "ltimindtree"

}


PRODUCT_INDUSTRIES = {
    "software",
    "saas",
    "fintech",
    "e-commerce",
    "healthtech",
    "adtech",
    "gaming",
    "ai/ml",
    "conversational ai"
}


GOOD_TITLE_KEYWORDS = {

    "machine learning engineer",
    "ml engineer",
    "ai engineer",
    "nlp engineer",
    "search engineer",
    "relevance engineer",
    "backend engineer",
    "data scientist",
    "applied scientist",
    "data engineer",
    "machine learning scientist"

}
NEGATIVE_CAREER_TERMS = {

    "test automation",
    "manual testing",
    "qa",
    "mobile development",
    "android",
    "ios",
    "devops",
    "cloud infrastructure",
    "selenium",
    "automation testing",
    "test cases",
    "qa engineer",
    "ui automation",
    "frontend",
    "react native",
    "flutter",
    "microservices",
    "crm",
    "erp",
    "support engineer",
    "helpdesk"
}


BAD_TITLES = {

    "marketing manager",
    "operations manager",
    "customer support",
    "graphic designer",
    "seo specialist",
    "sales manager",
    "brand manager",
    "content writer",
    "hr manager",
    "accountant",
    "civil engineer"

}


NEGATIVE_DOMAINS = {

    "computer vision",
    "speech",
    "robotics"

}


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
    "vector database",
    "sentence transformers"

}


# ==========================================================
# MAIN SCORER
# ==========================================================
def career_fit_score(candidate_features):

    score = 0.50

    # =====================================================
    # EXPERIENCE SWEET SPOT
    # =====================================================

    years_exp = candidate_features.get(
        "years_experience",
        0
    )

    if 5 <= years_exp <= 9:
        score += 0.20

    elif 3 <= years_exp < 5:
        score += 0.10

    elif years_exp < 3:
        score -= 0.20

    elif years_exp > 15:
        score -= 0.10

    # =====================================================
    # TITLE RELEVANCE
    # =====================================================

    current_title = candidate_features.get(
        "current_title",
        ""
    ).lower()

    job_titles = [

        title.lower()

        for title in candidate_features.get(
            "job_titles",
            []
        )

    ]

    all_titles = " ".join(
        job_titles + [current_title]
    )

    has_good_title = any(

        keyword in all_titles

        for keyword in GOOD_TITLE_KEYWORDS

    )

    has_bad_title = any(

        bad_title in all_titles

        for bad_title in BAD_TITLES

    )

    if has_good_title:
        score += 0.20

    if has_bad_title:
        score -= 0.70

    # =====================================================
    # PRODUCT COMPANY EXPERIENCE
    # =====================================================

    industries = [

        industry.lower()

        for industry in candidate_features.get(
            "industries_worked",
            []
        )

    ]

    product_count = sum(

        1

        for industry in industries

        if industry in PRODUCT_INDUSTRIES

    )

    score += min(
        product_count * 0.05,
        0.15
    )

    # =====================================================
    # CONSULTING ONLY PENALTY
    # =====================================================

    companies = [

        company.lower()

        for company in candidate_features.get(
            "companies",
            []
        )

    ]

    if len(companies) > 0:

        consulting_count = sum(

            1

            for company in companies

            if any(

                consulting in company

                for consulting in
                CONSULTING_COMPANIES

            )

        )

        consulting_ratio = (
            consulting_count /
            len(companies)
        )

        if consulting_ratio >= 0.80:
            score -= 0.25

    # =====================================================
    # CAREER TEXT
    # =====================================================

    career_text = " ".join(

        candidate_features.get(
            "career_descriptions",
            []
        )

    ).lower()

    # =====================================================
    # PRODUCTION EVIDENCE
    # =====================================================

    evidence_matches = sum(

        1

        for keyword in PRODUCTION_EVIDENCE

        if keyword in career_text

    )

    score += min(
        evidence_matches * 0.06,
        0.30
    )

    # =====================================================
    # STRONG SEARCH / RANKING SIGNALS
    # =====================================================

    signal_matches = sum(

        1

        for term in HIGH_SIGNAL_TERMS

        if term in career_text

    )

    score += min(
        signal_matches * 0.12,
        0.50
    )

    # =====================================================
    # NEGATIVE CAREER TERMS
    # =====================================================

    negative_matches = sum(

        1

        for term in NEGATIVE_CAREER_TERMS

        if term in career_text

    )

    if (
        negative_matches >= 3
        and signal_matches == 0
    ):

        score -= 0.40

    # =====================================================
    # KEYWORD STUFFING DETECTION
    # =====================================================

    candidate_skills = set(

        skill.lower()

        for skill in candidate_features.get(
            "skill_names",
            []
        )

    )

    claimed_ai_skills = (

        candidate_skills.intersection(
            AI_SKILLS
        )

    )

    if len(claimed_ai_skills) >= 3:

        evidence_found = any(

            keyword in career_text

            for keyword in PRODUCTION_EVIDENCE

        )

        if (

            not evidence_found

            and

            not has_good_title

        ):

            if len(claimed_ai_skills) >= 5:
                score -= 0.60

            else:
                score -= 0.35

    # =====================================================
    # DOMAIN MISMATCH
    # =====================================================

    negative_industries = [

        industry

        for industry in industries

        if any(

            domain in industry

            for domain in NEGATIVE_DOMAINS

        )

    ]

    if len(industries) > 0:

        ratio = (

            len(negative_industries)
            / len(industries)

        )

        if ratio >= 0.70:
            score -= 0.30

    # =====================================================
    # JOB HOPPING
    # =====================================================

    num_companies = candidate_features.get(
        "num_companies",
        0
    )

    if years_exp > 0:

        jobs_per_year = (
            num_companies /
            years_exp
        )

        if jobs_per_year > 1:
            score -= 0.15

    # =====================================================
    # NORMALIZE
    # =====================================================

    score = max(
        0.0,
        min(score, 1.0)
    )

    return score