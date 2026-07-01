from collections import defaultdict


class DiversityReranker:

    def rerank(
            self,
            ranked_candidates,
            candidate_features,
            top_k=100
    ):

        final_results = []

        title_counts = defaultdict(int)

        MAX_PER_TITLE = 15

        feature_map = {

            feature["candidate_id"]: feature

            for feature in candidate_features

        }

        for candidate in ranked_candidates:

            candidate_id = candidate[
                "candidate_id"
            ]

            feature = feature_map[
                candidate_id
            ]

            title = feature[
                "current_title"
            ].lower()

            if (
                    title_counts[title]
                    < MAX_PER_TITLE
            ):

                final_results.append(
                    candidate
                )

                title_counts[title] += 1

            if len(final_results) >= top_k:

                break

        return final_results