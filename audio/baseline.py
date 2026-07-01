class AdaptiveBaseline:

    def __init__(self):
        self.values = []
        self.max_samples = 30

    def update(self, current_level):

        self.values.append(current_level)

        if len(self.values) > self.max_samples:
            self.values.pop(0)

        baseline = sum(self.values) / len(self.values)

        return baseline