import numpy as np


class SoundMeter:

    def calculate(self, audio):

        rms = np.sqrt(np.mean(audio ** 2))

        return rms 