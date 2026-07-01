class TemporalAnalysis:

    def calculate(self, rms_history):

        if len(rms_history) < 2:
            return 0

        changes = []

        for i in range(1, len(rms_history)):

            diff = abs(rms_history[i] - rms_history[i - 1])

            changes.append(diff)

        average_change = sum(changes) / len(changes)

        score = min(100, average_change * 20000)

        return round(score, 1)