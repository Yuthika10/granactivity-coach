"""Risk test 3: can the laptop speak Hindi offline?

Needs:  pip install pyttsx3
Run from the repo root with the venv active:
    python checks\\test_tts.py
"""
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")

print("Voices installed on this computer:")
hindi = None
for v in voices:
    print(" -", v.name)
    if "hindi" in v.name.lower() or "hi-in" in v.id.lower() or "kalpana" in v.name.lower() or "hemant" in v.name.lower():
        hindi = v

engine.setProperty("rate", 140)  # slower speech for elderly listeners

if hindi:
    print(f"\nUsing Hindi voice: {hindi.name}")
    engine.setProperty("voice", hindi.id)
    engine.say("नमस्ते नानी! आज हम थोड़ी हल्की कसरत करेंगे। आप तैयार हैं?")
else:
    print("\nNo Hindi voice found. Speaking a test in the default voice instead.")
    engine.say("No Hindi voice found. We will need another text to speech option.")

engine.runAndWait()