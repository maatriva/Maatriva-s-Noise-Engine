from noise.event_manager import EventManager
from audio.recorder import AudioRecorder
from audio.baseline import AdaptiveBaseline
from audio.event_detector import NoiseEventDetector
from audio.logger import EventLogger
from audio.features import FeatureExtractor
from audio.disturbance import DisturbanceScore
from algorithm.temporal_analysis import TemporalAnalysis
from algorithm.pattern_analysis import PatternAnalysis
from algorithm.frequency_analysis import FrequencyAnalysis
from algorithm.persistence_analysis import PersistenceAnalysis
from algorithm.decision_engine import DecisionEngine


# ==========================================
# Initialize Modules
# ==========================================

recorder = AudioRecorder()
feature_extractor = FeatureExtractor()
baseline_engine = AdaptiveBaseline()
event_manager = EventManager()

detector = NoiseEventDetector()

disturbance = DisturbanceScore()
frequency_analysis = FrequencyAnalysis()
persistence_analysis = PersistenceAnalysis()
decision_engine = DecisionEngine()
temporal_analysis = TemporalAnalysis()
pattern_analysis = PatternAnalysis()
logger = EventLogger()


# ==========================================
# Initial Baseline
# ==========================================

baseline = 0.0

print("=" * 50)
print("MAATRIVA NOISE ENGINE v0.1")
print("=" * 50)
print("Learning room environment...\n")

for i in range(10):

    audio = recorder.record(duration=0.5)

    features = feature_extractor.extract(audio)

    current_level = features.rms

    if current_level < 0.01:
        baseline = baseline_engine.update(current_level)
    else:
        print("Ignoring noisy calibration sample...")

    print(f"Learning {i+1}/10  Baseline : {baseline:.6f}")

print("\nBaseline Learning Complete.")
print("=" * 50)


# ==========================================
# Main Loop
# ==========================================

while True:

    # --------------------------------------
    # Record Audio
    # --------------------------------------

    audio = recorder.record(duration=0.5)

    # --------------------------------------
    # Extract Features
    # --------------------------------------

    features = feature_extractor.extract(audio)

    current_level = features.rms
    peak = features.peak
    duration = features.duration
    zcr = features.zcr
    energy = features.energy
    spectral_centroid = features.spectral_centroid

    # --------------------------------------
    # Frequency Analysis
    # --------------------------------------

    frequency_score = frequency_analysis.calculate(
        spectral_centroid,
        zcr
    )

    # --------------------------------------
    # Detect Noise Event
    # --------------------------------------

    event, ratio = detector.detect(
        current_level,
        baseline
    )

    # --------------------------------------
    # Update Baseline
    # --------------------------------------

    if not event:
        baseline = baseline_engine.update(current_level)

    # --------------------------------------
    # Disturbance Score
    # --------------------------------------

    if event:
     disturbance_score = disturbance.calculate(
        ratio,
        peak,
        duration
    )
    else:
     disturbance_score = 0.0

    # --------------------------------------
    # Event Manager
    # --------------------------------------

    completed_event = event_manager.update(
    event,
    current_level,
    baseline,
    peak,
    zcr,
    energy,
    spectral_centroid,
    frequency_score,
    disturbance_score
)

    if completed_event is not None:

    # ----------------------------------
    # Persistence Score
    # ----------------------------------
        persistence_score = persistence_analysis.calculate(
            completed_event.audio_duration,
            completed_event.elapsed_time,
            completed_event.samples
        )

        # ----------------------------------
        # Temporal Score
        # ----------------------------------
        temporal_score = temporal_analysis.calculate(
            completed_event.rms_history
        )

        # ----------------------------------
        # Pattern Analysis
        # ----------------------------------
        pattern = pattern_analysis.classify(
            completed_event.rms_history,
            temporal_score,
            persistence_score
        )

        # ----------------------------------
        # Decision Engine
        # ----------------------------------
        final_score, risk = decision_engine.evaluate(
            completed_event,
            persistence_score,
            temporal_score
        )

        # ----------------------------------
        # Store results in the event
        # ----------------------------------
        completed_event.persistence_score = persistence_score
        completed_event.temporal_score = temporal_score
        completed_event.pattern = pattern
        completed_event.final_score = final_score
        completed_event.risk_level = risk

        # ----------------------------------
        # PRINT DECISION ENGINE HERE 👇
        # ----------------------------------
        print("\n" + "=" * 45)
        print("          DECISION ENGINE")
        print("=" * 45)

        print(f"Loudness Score      : {completed_event.max_disturbance_score:.1f}")
        print(f"Frequency Score     : {completed_event.average_frequency_score:.1f}")
        print(f"Persistence Score   : {completed_event.persistence_score:.1f}")
        print(f"Temporal Score      : {completed_event.temporal_score:.1f}")
        print(f"Pattern             : {completed_event.pattern}")

        print("-" * 45)

        print(f"Final Score         : {completed_event.final_score:.1f}")
        print(f"Risk Level          : {completed_event.risk_level}")

        print("=" * 45)

        # ----------------------------------
        # Save Event
        # ----------------------------------
        logger.log_event(completed_event)

        print("\n✅ Event saved successfully!")
    # --------------------------------------
    # Frame Logger
    # --------------------------------------

    logger.log(
        current_level,
        baseline,
        ratio,
        event
    )

    # --------------------------------------
    # Status
    # --------------------------------------

    if disturbance_score == 0:
     status = "NO EVENT"

    elif disturbance_score < 30:
     status = "LOW"

    elif disturbance_score < 60:
        status = "MODERATE"

    elif disturbance_score < 80:
        status = "HIGH"

    else:
        status = "CRITICAL"

    # --------------------------------------
    # Display
    # --------------------------------------

    print("\n" + "=" * 55)
    print("          MAATRIVA NOISE ENGINE")
    print("=" * 55)

    print(f"Current Level        : {current_level:.6f}")
    print(f"Baseline             : {baseline:.6f}")
    print(f"Ratio                : {ratio:.2f}x")
    print(f"Peak Level           : {peak:.4f}")
    print(f"Zero Crossing Rate   : {zcr:.4f}")
    print(f"Energy               : {energy:.6f}")
    print(f"Spectral Centroid    : {spectral_centroid:.2f} Hz")
    print(f"Frequency Score      : {frequency_score}/100")
    print(f"Duration             : {duration:.2f} sec")

    print()

    if event:
        print("Noise Event          : YES 🔴")
    else:
        print("Noise Event          : NO 🟢")
     
    if disturbance_score == 0:
     print("Disturbance Score    : --")
    else:
        print(f"Disturbance Score    : {disturbance_score:.1f}/100")
        print(f"Status               : {status}")

    if event:

        print("\nReason:")

        print(f"✓ Sound is {ratio:.2f}x above baseline")

        if peak > 0.20:
            print("✓ High peak detected")

        if duration >= 0.5:
            print("✓ Noise persisted")

    print("=" * 55)