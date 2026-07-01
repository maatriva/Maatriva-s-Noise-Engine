class DecisionEngine:

    def evaluate(
        self,
        event,
        persistence_score,
        temporal_score
    ):

        loudness_score = event.max_disturbance_score
        frequency_score = event.average_frequency_score

        final_score = (
            loudness_score * 0.40 +
            frequency_score * 0.20 +
            persistence_score * 0.20 +
            temporal_score * 0.20
        )

        if final_score < 25:
            level = "SAFE"
        elif final_score < 50:
            level = "LOW"
        elif final_score < 70:
            level = "MODERATE"
        elif final_score < 85:
            level = "HIGH"
        else:
            level = "CRITICAL"

        return round(final_score, 1), level