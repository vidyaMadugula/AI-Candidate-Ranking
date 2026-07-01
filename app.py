import streamlit as st
import pandas as pd
import time

from preprocess import preprocess_candidates
from rank import CandidateRanker

# ======================================================
# PAGE CONFIG
# ======================================================

def generate_csv_reasoning(candidate):

    features = candidate.get(
        "candidate_features",
        {}
    )

    title = features.get(
        "current_title",
        "Candidate"
    )

    years = round(
        features.get(
            "years_experience",
            0
        ),
        1
    )

    skills = features.get(
        "skill_names",
        []
    )[:3]

    skill_text = ", ".join(
        skills
    ) if skills else "relevant skills"

    response_rate = features.get(
        "response_rate",
        None
    )

    reasoning = (

        f"{title} with {years} years of experience; "
        f"strong background in {skill_text}"
    )

    if response_rate is not None:

        reasoning += (
            f"; recruiter response rate "
            f"{response_rate:.2f}"
        )

    reasoning += "."

    return reasoning

st.set_page_config(

    page_title="Intelligent Candidate Ranker",

    page_icon="🎯",

    layout="wide"

)

# ======================================================
# HEADER
# ======================================================

st.title(
    "🎯 Intelligent Candidate Ranker"
)

st.markdown(
    """
### Explainable AI Candidate Ranking Demo

This demo ranks a preloaded sample and displays the **Top candidates**
using:

- Hybrid Retrieval (Semantic + BM25)
- Career Intelligence Signals
- Behavioral Signals
- Profile Quality Assessment
- Honeypot Detection
- Explainable Ranking
"""
)

st.markdown("---")

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("Demo Dataset")

st.sidebar.success(
    "Displaying Top Candidates"
)

run_button = st.sidebar.button(
    "🚀 Run Ranking Demo"
)

# ======================================================
# RUN DEMO
# ======================================================

if run_button:

    start = time.time()

    sample_file = (
        "data/demo_candidates.jsonl"
    )

    with st.spinner(
            "Processing and ranking candidates..."
    ):

        # Preprocess sample dataset

        preprocess_candidates(
            sample_file,
            output_dir="data/demo_processed",
            max_candidates=100
        )

        ranker = CandidateRanker(data_dir="data/demo_processed")

        # Demo JD

        job_description = """

        Senior AI Engineer with experience in
        Retrieval-Augmented Generation,
        semantic search, embeddings,
        vector databases, ranking systems,
        recommendation systems and Python.

        """

        required_skills = [

            "python",
            "rag",
            "faiss",
            "embeddings",
            "retrieval",
            "ranking",
            "semantic search",
            "langchain"

        ]

        mandatory_skills = [

            "python",
            "rag"

        ]

        results = ranker.rank(

            job_description=job_description,

            required_skills=required_skills,

            mandatory_skills=mandatory_skills,

            min_experience=5,

            top_k=100

        )

    elapsed = round(
        time.time() - start,
        2
    )

    st.success(
        f"Ranking completed successfully in {elapsed} seconds"
    )

    st.markdown("---")

    # ==================================================
    # SUMMARY METRICS
    # ==================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Candidates Displayed",
            min(len(results), 50)
        )

    with col2:

        st.metric(
            "Top Score",
            round(
                results[0]["final_score"],
                3
            )
        )

    with col3:

        st.metric(
            "Runtime (sec)",
            elapsed
        )

    st.markdown("---")

    st.header(
        "🏆 Top Ranked Candidates"
    )

    csv_rows = []

    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    for rank, candidate in enumerate(
            results[:50],
            start=1
    ):

        explanation = candidate.get(
            "explanation",
            []
        )

        reasoning = generate_csv_reasoning(
            candidate
        )

        with st.expander(

                f"#{rank} | "
                f"{candidate['candidate_id']} | "
                f"Score: "
                f"{candidate['final_score']:.3f}"

        ):

            # ------------------------------------------
            # Main Metrics
            # ------------------------------------------

            col1, col2 = st.columns(
                [1, 3]
            )

            with col1:

                st.metric(

                    label="Final Score",

                    value=round(

                        candidate[
                            "final_score"
                        ],

                        3

                    )

                )

            with col2:

                st.markdown(
                    "### Why this candidate?"
                )

                if explanation:

                    for exp in explanation[:3]:

                        st.success(exp)

                else:

                    st.info(
                        "No explanation available."
                    )

            st.markdown("---")

            # ------------------------------------------
            # Component Scores
            # ------------------------------------------

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(

                    "Semantic Match",

                    round(

                        candidate.get(
                            "semantic_score",
                            0
                        ),

                        2

                    )

                )

                st.metric(

                    "Skill Match",

                    round(

                        candidate.get(
                            "skill_score",
                            0
                        ),

                        2

                    )

                )

            with c2:

                st.metric(

                    "Career Fit",

                    round(

                        candidate.get(
                            "career_fit_score",
                            0
                        ),

                        2

                    )

                )

                st.metric(

                    "Behavior Score",

                    round(

                        candidate.get(
                            "behavior_score",
                            0
                        ),

                        2

                    )

                )

            with c3:

                st.metric(

                    "Profile Quality",

                    round(

                        candidate.get(
                            "profile_quality_score",
                            0
                        ),

                        2

                    )

                )

                st.metric(

                    "Honeypot Penalty",

                    round(

                        candidate.get(
                            "honeypot_penalty",
                            1
                        ),

                        2

                    )

                )

        # ----------------------------------------------
        # CSV rows
        # ----------------------------------------------

        csv_rows.append({

            "candidate_id":
                candidate[
                    "candidate_id"
                ],

            "rank":
                rank,

            "score":
                round(

                    candidate[
                        "final_score"
                    ],

                    6

                ),

            "reasoning":
                reasoning

        })

    # ==================================================
    # DOWNLOAD CSV
    # ==================================================

    st.markdown("---")

    submission = pd.DataFrame(
        csv_rows
    )

    csv = submission.to_csv(
        index=False
    )

    st.download_button(

        label="📥 Download Ranked CSV",

        data=csv,

        file_name="submission.csv",

        mime="text/csv"

    )

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "Hybrid Retrieval • Career Intelligence • "
    "Behavior Signals • Honeypot Detection"
)