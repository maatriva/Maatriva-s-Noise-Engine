from dataclasses import dataclass


@dataclass
class FeatureVector:

    rms: float
    peak: float
    duration: float

    zcr: float
    energy: float

    spectral_centroid: float