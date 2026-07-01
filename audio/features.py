import numpy as np
from scipy.fft import rfft, rfftfreq
from models.feature_vector import FeatureVector

class FeatureExtractor:

    def extract(self, audio):

        # Root Mean Square (Loudness)
        rms = np.sqrt(np.mean(audio ** 2))

        # Total signal energy
        energy = np.sum(audio ** 2)

        # -------------------------
        # Spectral Centroid
        # -------------------------

        fft = np.abs(rfft(audio.flatten()))

        freqs = rfftfreq(len(audio), 1 / 44100)

        if np.sum(fft) > 0:
            spectral_centroid = np.sum(freqs * fft) / np.sum(fft)
        else:
            spectral_centroid = 0.0

        # Maximum amplitude
        peak = np.max(np.abs(audio))

        # Audio duration
        duration = len(audio) / 44100

        # -------------------------
        # Zero Crossing Rate (ZCR)
        # -------------------------

        zero_crossings = np.sum(
            np.diff(np.sign(audio.flatten())) != 0
        )

        zcr = zero_crossings / len(audio)

        return FeatureVector(
        rms=float(rms),
        peak=float(peak),
        duration=duration,
        zcr=float(zcr),
        energy=float(energy),
        spectral_centroid=float(spectral_centroid)
    )