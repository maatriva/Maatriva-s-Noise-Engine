class DisturbanceScore:

    def calculate(self, ratio, peak, duration):

        score = 0

        score += min(ratio * 15, 50)

        score += min(peak * 300, 30)

        score += min(duration * 10, 20)

        return round(min(score, 100), 1)