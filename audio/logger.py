from datetime import datetime
import csv
import os


class EventLogger:

    def __init__(self):

        self.file = "logs/noise_events.csv"
        self.event_file = "logs/noise_event_summary.csv"

        os.makedirs("logs", exist_ok=True)

        # ----------------------------
        # Frame-by-frame Log
        # ----------------------------
        if not os.path.exists(self.file):

            with open(self.file, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Timestamp",
                    "Current_Level",
                    "Baseline",
                    "Ratio",
                    "Noise_Event"
                ])

        # ----------------------------
        # Event Summary Log
        # ----------------------------
        if not os.path.exists(self.event_file):

            with open(self.event_file, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Start_Time",
                    "End_Time",
                    "Elapsed_Time",
                    "Audio_Duration",

                    "Peak_RMS",
                    "Average_RMS",
                    "Max_Peak",

                    "Average_ZCR",
                    "Average_Energy",
                    "Average_Spectral_Centroid",

                    "Average_Frequency_Score",
                    "Max_Disturbance_Score",

                    "Persistence_Score",
                    "Temporal_Score",

                    "Pattern",

                    "Final_Score",
                    "Risk_Level",

                    "Baseline",
                    "Samples",
                    "Severity"
                ])
                   

    # =========================================
    # Frame Logger
    # =========================================

    def log(self, current, baseline, ratio, event):

        with open(self.file, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now(),
                current,
                baseline,
                ratio,
                event
            ])

    # =========================================
    # Event Logger
    # =========================================

    def log_event(self, event):

        with open(self.event_file, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                event.start_time,
                event.end_time,
                event.elapsed_time,
                event.audio_duration,

                event.peak_rms,
                event.average_rms,
                event.max_peak,

                event.average_zcr,
                event.average_energy,
                event.average_spectral_centroid,

                event.average_frequency_score,
                event.max_disturbance_score,

                event.persistence_score,
                event.temporal_score,

                event.pattern,

                event.final_score,
                event.risk_level,

                event.baseline,
                event.samples,
                event.severity
            ])