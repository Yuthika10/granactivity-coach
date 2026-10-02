"""Risk test 2: can we transcribe spoken Hindi offline?

Run from the repo root with the venv active:
    python checks\\test_stt.py
The first run downloads the Whisper 'small' model (~500 MB).
"""
import os
import time

import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
SECONDS = 6
OUT = os.path.join("recordings", "test_input.wav")  # recordings/ is gitignored

print("Loading Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")

input(f"Press Enter, then speak in Hindi for {SECONDS} seconds...")
print("Recording...")
audio = sd.rec(int(SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
sd.wait()
print("Done recording.")

os.makedirs("recordings", exist_ok=True)
sf.write(OUT, audio, SAMPLE_RATE)

start = time.time()
segments, info = model.transcribe(OUT, language="hi")
text = " ".join(seg.text.strip() for seg in segments)
print(f"\n[{time.time() - start:.1f}s] Transcript: {text}")