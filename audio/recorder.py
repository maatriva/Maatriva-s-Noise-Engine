import sounddevice as sd
import numpy as np


class AudioRecorder:

    def __init__(self):
        self.sample_rate = 44100
        self.channels = 2
        self.device = 1

    def record(self, duration=0.5):

        print(f"\n🎤 Recording for {duration} seconds...")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            device=self.device
        )

        sd.wait()

        print("✅ Recording Finished")

        # Convert int16 → float32
        audio = audio.astype(np.float32) / 32768.0

        # Convert stereo → mono
        audio = np.mean(audio, axis=1)

        return audio