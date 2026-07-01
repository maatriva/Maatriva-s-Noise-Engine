from noise.event_manager import EventManager
from audio.recorder import AudioRecorder
from audio.baseline import AdaptiveBaseline
from audio.event_detector import NoiseEventDetector
from audio.logger import EventLogger
from audio.features import FeatureExtractor
from audio.disturbance import DisturbanceScore


# ===========================
# Initialize Modules
# ===========================

recorder = AudioRecorder()
feature_extractor = FeatureExtractor()
baseline_engine = AdaptiveBaseline()
event_manager = EventManager()
detector = NoiseEventDetector()
disturbance = DisturbanceScore()
logger = EventLogger()


# ===========================
# Initial Baseline
# ===========================

baseline = 0.0


print("=" * 50)
print("MAATRIVA NOISE ENGINE v0.1")
print("=" * 50)
print("Learning room environment...\n")

# Learn baseline using first 10 samples
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


# ===========================
# Main Loop
# ===========================

while True:

    # Record Audio
    audio = recorder.record(duration=0.5)

    # Extract Features
    features = feature_extractor.extract(audio)

    current_level = features.rms
    peak = features.peak
    duration = features.duration
    zcr = features.zcr
    energy = features.energy
    spectral_centroid = features.spectral_centroid

    # Detect Noise Event
    event, ratio = detector.detect(current_level, baseline)

    # Update baseline ONLY if no event
    if not event:
        baseline = baseline_engine.update(current_level)

    # Calculate disturbance only if event detected
    if event:
        score = disturbance.calculate(
            ratio,
            peak,
            duration
        )
    else:
        score = None

    completed_event = event_manager.update(
    event,
    current_level,
    baseline,
    peak,
    zcr,
    energy,
    spectral_centroid
)

    if completed_event:

     logger.log_event(completed_event)

     print("\n✅ Event saved successfully!")

# Logger (frame-by-frame log)
    logger.log(
    current_level,
    baseline,
    ratio,
    event
)

    # Status
    if score is None:
        status = "NO EVENT"

    elif score < 30:
        status = "LOW"

    elif score < 60:
        status = "MODERATE"

    elif score < 80:
        status = "HIGH"

    else:
        status = "CRITICAL"

    # ===========================
    # Display
    # ===========================

    print("\n" + "=" * 55)
    print("          MAATRIVA NOISE ENGINE")
    print("=" * 55)

    print(f"Current Level       : {current_level:.6f}")
    print(f"Baseline            : {baseline:.6f}")
    print(f"Ratio               : {ratio:.2f}x")
    print(f"Peak Level          : {peak:.4f}")
    print(f"Zero Crossing Rate : {zcr:.4f}")
    print(f"Energy              : {energy:.6f}")
    print(f"Spectral Centroid : {spectral_centroid:.2f} Hz")
    print(f"Duration            : {duration:.2f} sec")

    print()

    if event:
        print("Noise Event         : YES 🔴")
    else:
        print("Noise Event         : NO 🟢")

    if score is None:
        print("Disturbance Score   : --")
    else:
        print(f"Disturbance Score   : {score:.1f}/100")

    print(f"Status              : {status}")

    # Explainability
    if event:
        print("\nReason:")
        print(f"✓ Sound is {ratio:.2f}x above baseline")

        if peak > 0.20:
            print("✓ High peak detected")

        if duration >= 0.5:
            print("✓ Noise persisted")

    print("=" * 55)