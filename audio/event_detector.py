class NoiseEventDetector:

    def __init__(self, threshold=2.5):
        self.threshold = threshold

    def detect(self, current_level, baseline):

        if baseline <= 0:
            return False, 1.0

        ratio = current_level / baseline

        print(
            f"DEBUG -> Current: {current_level:.6f} | "
            f"Baseline: {baseline:.6f} | "
            f"Ratio: {ratio:.2f}"
        )

        event = ratio >= self.threshold

        return event, ratio