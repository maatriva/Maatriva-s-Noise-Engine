from dataclasses import dataclass


@dataclass
class NoiseEvent:

    # -------------------------
    # Time Information
    # -------------------------
    start_time: float
    end_time: float

    elapsed_time: float
    audio_duration: float

    # -------------------------
    # Loudness Features
    # -------------------------
    peak_rms: float
    average_rms: float

    max_peak: float

    # -------------------------
    # Spectral Features
    # -------------------------
    average_zcr: float
    average_energy: float
    average_spectral_centroid: float

    # -------------------------
    # Event Information
    # -------------------------
    baseline: float
    samples: int
    severity: str