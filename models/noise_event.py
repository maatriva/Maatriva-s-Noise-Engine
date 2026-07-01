from dataclasses import dataclass

@dataclass
class NoiseEvent:

    start_time: float
    end_time: float

    elapsed_time: float
    audio_duration: float

    peak_rms: float
    average_rms: float

    max_peak: float

    average_zcr: float
    average_energy: float
    average_spectral_centroid: float

    average_frequency_score: float
    max_disturbance_score: float

    baseline: float
    samples: int

    severity: str
    pattern: str

    rms_history: list
    average_frequency_score: float
    max_disturbance_score: float

    persistence_score: float
    temporal_score: float

    final_score: float
    risk_level: str

    pattern: str

    rms_history: list