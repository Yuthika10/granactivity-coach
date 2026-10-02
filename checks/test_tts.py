"""Risk test 3 (Piper): can the laptop speak Hindi offline?

Setup (venv active, from repo root):
    pip install piper-tts
    mkdir voices && cd voices
    python -m piper.download_voices hi_IN-priyamvada-medium
    cd ..
Run:
    python checks\\test_tts_piper.py
"""
import os
import time
import wave
import winsound

from piper import PiperVoice

VOICE_PATH = os.path.join("voices", "hi_IN-priyamvada-medium.onnx")
OUT = os.path.join("recordings", "tts_test.wav")  # recordings/ is gitignored
TEXT = "नमस्ते नानी! आज हम थोड़ी हल्की कसरत करेंगे। आप तैयार हैं?"

if not os.path.exists(VOICE_PATH):
    raise SystemExit(f"Voice not found at {VOICE_PATH}. Run the download step first.")

print("Loading voice...")
voice = PiperVoice.load(VOICE_PATH)

os.makedirs("recordings", exist_ok=True)
start = time.time()
with wave.open(OUT, "wb") as wav_file:
    voice.synthesize_wav(TEXT, wav_file)
print(f"Generated speech in {time.time() - start:.1f}s, playing now...")

winsound.PlaySound(OUT, winsound.SND_FILENAME)
print("Done.")