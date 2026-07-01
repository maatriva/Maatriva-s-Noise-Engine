from models.noise_event import NoiseEvent
import time


class EventManager:

    def __init__(self):

        # -------------------------
        # Event Status
        # -------------------------
        self.event_active = False
        self.start_time = None

        # -------------------------
        # Quiet Frame Logic
        # -------------------------
        self.quiet_counter = 0
        self.end_threshold = 3

        # -------------------------
        # RMS Statistics
        # -------------------------
        self.max_rms = 0.0
        self.sum_rms = 0.0
        self.samples = 0

        # -------------------------
        # Peak Statistics
        # -------------------------
        self.max_peak = 0.0

        # -------------------------
        # Feature Statistics
        # -------------------------
        self.sum_zcr = 0.0
        self.sum_energy = 0.0
        self.sum_centroid = 0.0

    def update(
        self,
        event,
        current_level,
        baseline,
        peak,
        zcr,
        energy,
        spectral_centroid
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

            self.max_peak = peak

            self.sum_zcr = zcr
            self.sum_energy = energy
            self.sum_centroid = spectral_centroid

            print("\n🚨 Noise Event Started")

            return None

        # ==================================
        # EVENT CONTINUES
        # ==================================
        elif event and self.event_active:

            self.quiet_counter = 0

            self.samples += 1

            self.sum_rms += current_level
            self.sum_zcr += zcr
            self.sum_energy += energy
            self.sum_centroid += spectral_centroid

            if current_level > self.max_rms:
                self.max_rms = current_level

            if peak > self.max_peak:
                self.max_peak = peak

            return None

        # ==================================
        # QUIET FRAME
        # ==================================
        elif not event and self.event_active:

            self.quiet_counter += 1

            print(f"Quiet Frame {self.quiet_counter}/{self.end_threshold}")

            if self.quiet_counter >= self.end_threshold:

                self.event_active = False

                end_time = time.time()

                elapsed_time = end_time - self.start_time

                average_rms = self.sum_rms / self.samples
                average_zcr = self.sum_zcr / self.samples
                average_energy = self.sum_energy / self.samples
                average_centroid = self.sum_centroid / self.samples

                # ---------------------------------
                # Temporary Severity Rule
                # ---------------------------------
                if average_rms < baseline * 3:
                    severity = "LOW"

                elif average_rms < baseline * 6:
                    severity = "MODERATE"

                elif average_rms < baseline * 10:
                    severity = "HIGH"

                else:
                    severity = "CRITICAL"

                # ---------------------------------
                # Create Noise Event
                # ---------------------------------
                completed_event = NoiseEvent(
                    start_time=self.start_time,
                    end_time=end_time,
                    elapsed_time=elapsed_time,
                    audio_duration=self.samples * 0.5,

                    peak_rms=self.max_rms,
                    average_rms=average_rms,
                    max_peak=self.max_peak,

                    average_zcr=average_zcr,
                    average_energy=average_energy,
                    average_spectral_centroid=average_centroid,

                    baseline=baseline,
                    samples=self.samples,
                    severity=severity
                )

                # ---------------------------------
                # Reset Everything
                # ---------------------------------
                self.quiet_counter = 0

                self.max_rms = 0.0
                self.sum_rms = 0.0

                self.max_peak = 0.0

                self.sum_zcr = 0.0
                self.sum_energy = 0.0
                self.sum_centroid = 0.0

                self.samples = 0

                return completed_event

            return None

        return None