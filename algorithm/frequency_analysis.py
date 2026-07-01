class FrequencyAnalysis:

    def calculate(
        self,
        spectral_centroid,
        zcr
    ):

        score = 0

        # --------------------
        # Spectral Centroid
        # --------------------

        if spectral_centroid < 3000:
            score += 10

        elif spectral_centroid < 6000:
            score += 30

        elif spectral_centroid < 9000:
            score += 50

        elif spectral_centroid < 12000:
            score += 70

        else:
            score += 90

        # --------------------
        # Zero Crossing Rate
        # --------------------

        if zcr < 0.03:
            score += 5

        elif zcr < 0.05:
            score += 10

        elif zcr < 0.08:
            score += 20

        else:
            score += 30

        return min(score, 100)