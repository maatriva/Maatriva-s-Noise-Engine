class PatternAnalysis:

    def classify(
        self,
        rms_history,
        temporal_score,
        persistence_score
    ):

        # Default
        pattern = "UNKNOWN"

        # -----------------------------
        # Continuous
        # -----------------------------
        if persistence_score >= 80 and temporal_score < 25:
            pattern = "CONTINUOUS"

        # -----------------------------
        # Impulsive
        # -----------------------------
        elif persistence_score < 40 and temporal_score >= 70:
            pattern = "IMPULSIVE"

        # -----------------------------
        # Rhythmic
        # -----------------------------
        elif 40 <= persistence_score <= 80 and 40 <= temporal_score <= 70:
            pattern = "RHYTHMIC"

        # -----------------------------
        # Intermittent
        # -----------------------------
        elif temporal_score >= 70:
            pattern = "INTERMITTENT"

        return pattern