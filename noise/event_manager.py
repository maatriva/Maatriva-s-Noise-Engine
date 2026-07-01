from models.noise_event import NoiseEvent
import time


class EventManager:

    def __init__(self):

        # ==========================
        # Event Status
        # ==========================
        self.event_active = False
        self.start_time = None

        # ==========================
        # Quiet Frame Logic
        # ==========================
        self.quiet_counter = 0
        self.end_threshold = 3

        # ==========================
        # RMS Statistics
        # ==========================
        self.max_rms = 0.0
        self.sum_rms = 0.0
        self.samples = 0
        self.rms_history = []

        # ==========================
        # Peak Statistics
        # ==========================
        self.max_peak = 0.0

        # ==========================
        # Feature Statistics
        # ==========================
        self.sum_zcr = 0.0
        self.sum_energy = 0.0
        self.sum_centroid = 0.0

        # ==========================
        # Frequency Statistics
        # ==========================
        self.sum_frequency_score = 0.0

        # ==========================
        # Disturbance Statistics
        # ==========================
        self.max_disturbance_score = 0.0

    def update(
        self,
        event,
        current_level,
        baseline,
        peak,
        zcr,
        energy,
        spectral_centroid,
        frequency_score,
        disturbance_score,
    ):

        # ==================================
        # EVENT START
        # ==================================
        if event and not self.event_active:

            self.event_active = True
            self.start_time = time.time()

            self.quiet_counter = 0

            self.max_rms = current_level
            self.sum_rms = current_level
            self.samples = 1

            self.rms_history = [current_level]

            self.max_peak = peak

            self.sum_zcr = zcr
            self.sum_energy = energy
            self.sum_centroid = spectral_centroid

            self.sum_frequency_score = frequency_score

            self.max_disturbance_score = disturbance_score

            print("\n🚨 Noise Event Started")

            return None

        # ==================================
        # EVENT CONTINUES
        # ==================================
        elif event and self.event_active:

            self.quiet_counter = 0

            self.samples += 1

            self.sum_rms += current_level
            self.rms_history.append(current_level)

            self.sum_zcr += zcr
            self.sum_energy += energy
            self.sum_centroid += spectral_centroid

            self.sum_frequency_score += frequency_score

            if current_level > self.max_rms:
                self.max_rms = current_level

            if peak > self.max_peak:
                self.max_peak = peak

            if disturbance_score > self.max_disturbance_score:
                self.max_disturbance_score = disturbance_score

            return None
                # ==================================
        # QUIET FRAME
        # ==================================
        elif not event and self.event_active:

            self.quiet_counter += 1

            print(f"Quiet Frame {self.quiet_counter}/{self.end_threshold}")

            if self.quiet_counter >= self.end_threshold:

                print("\n🏁 Noise Event Completed")

                end_time = time.time()
                elapsed_time = end_time - self.start_time

                average_rms = self.sum_rms / self.samples
                average_zcr = self.sum_zcr / self.samples
                average_energy = self.sum_energy / self.samples
                average_centroid = self.sum_centroid / self.samples
                average_frequency_score = (
                    self.sum_frequency_score / self.samples
                )

                # ==================================
                # Temporary Severity Rule
                # ==================================
                ratio = average_rms / baseline if baseline > 0 else 1

                if ratio < 3:
                    severity = "LOW"
                elif ratio < 6:
                    severity = "MODERATE"
                elif ratio < 10:
                    severity = "HIGH"
                else:
                    severity = "CRITICAL"

                # ==================================
                # Create Noise Event
                # ==================================
                completed_event = NoiseEvent(

                    # -------------------------
                    # Time
                    # -------------------------
                    start_time=self.start_time,
                    end_time=end_time,
                    elapsed_time=elapsed_time,
                    audio_duration=self.samples * 0.5,

                    # -------------------------
                    # Loudness
                    # -------------------------
                    peak_rms=self.max_rms,
                    average_rms=average_rms,
                    max_peak=self.max_peak,

                    # -------------------------
                    # Spectral Features
                    # -------------------------
                    average_zcr=average_zcr,
                    average_energy=average_energy,
                    average_spectral_centroid=average_centroid,

                    # -------------------------
                    # Algorithm Scores
                    # -------------------------
                    average_frequency_score=average_frequency_score,
                    max_disturbance_score=self.max_disturbance_score,

                    persistence_score=0.0,
                    temporal_score=0.0,

                    final_score=0.0,
                    risk_level="UNKNOWN",
                    pattern="UNKNOWN",

                    # -------------------------
                    # Event Info
                    # -------------------------
                    baseline=baseline,
                    samples=self.samples,
                    severity=severity,

                    rms_history=self.rms_history.copy()
                )

                # ==================================
                # Reset Everything
                # ==================================
                self.event_active = False
                self.start_time = None

                self.quiet_counter = 0

                self.max_rms = 0.0
                self.sum_rms = 0.0

                self.max_peak = 0.0

                self.sum_zcr = 0.0
                self.sum_energy = 0.0
                self.sum_centroid = 0.0

                self.sum_frequency_score = 0.0
                self.max_disturbance_score = 0.0

                self.samples = 0
                self.rms_history = []

                return completed_event

            return None

        return None