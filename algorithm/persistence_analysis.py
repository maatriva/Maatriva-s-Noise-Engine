class PersistenceAnalysis:

    def calculate(
        self,
        audio_duration,
        elapsed_time,
        samples
    ):

        score = 0

        # -------------------------
        # Audio Duration
        # -------------------------

        if audio_duration < 1:
            score += 10

        elif audio_duration < 2:
            score += 30

        elif audio_duration < 4:
            score += 50

        elif audio_duration < 8:
            score += 70

        else:
            score += 90

        # -------------------------
        # Number of Frames
        # -------------------------

        if samples <= 2:
            score += 5

        elif samples <= 4:
            score += 10

        elif samples <= 8:
            score += 20

        else:
            score += 30

        return min(score, 100)