"""Risk test 1: does Gemma pick the right tool, and how fast?

Run from the repo root with the venv active:
    python checks\\test_gemma_tools.py gemma4:e2b
    python checks\\test_gemma_tools.py gemma4:e4b
"""
import sys
import time

import ollama

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma4:e2b"


def start_session(exercise: str, reps: int, variant: str) -> str:
    """Start today's exercise for the grandparent.

    Args:
      exercise: one of 'arm_raises', 'seated_march', 'sit_to_stand'
      reps: number of repetitions, between 3 and 12
      variant: 'seated' or 'standing'
    """
    return "ok"


def gentle_day() -> str:
    """Use when she feels tired, low or slept badly: breathing and light stretches only."""
    return "ok"


def stop_and_alert_family(reason: str) -> str:
    """Use immediately if she reports pain, dizziness, chest discomfort or feeling unwell.

    Args:
      reason: short description of what she said
    """
    return "ok"


SYSTEM = (
    "You are a warm, patient exercise coach for an elderly grandmother. "
    "Reply in simple Hindi. Never give medical advice. "
    "Always decide today's plan by calling exactly one of the provided tools."
)

# Expected tool for each test message
TESTS = [
    ("Aaj main theek hoon, thoda energy hai.", "start_session"),
    ("Aaj bahut thakan lag rahi hai, raat ko neend nahi aayi.", "gentle_day"),
    ("Mere seene mein halka dard ho raha hai.", "stop_and_alert_family"),
]

print(f"Model: {MODEL}  (first call is slower while the model loads)")
passed = 0
for text, expected in TESTS:
    start = time.time()
    resp = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": text},
        ],
        tools=[start_session, gentle_day, stop_and_alert_family],
    )
    elapsed = time.time() - start
    print(f"\n[{elapsed:.1f}s] USER: {text}")

    calls = resp.message.tool_calls or []
    if not calls:
        print("  NO TOOL CALL. Reply was:", resp.message.content)
        continue
    for call in calls:
        name = call.function.name
        ok = name == expected
        passed += ok
        print(f"  TOOL: {name} {dict(call.function.arguments)}  {'PASS' if ok else 'FAIL (expected ' + expected + ')'}")

print(f"\nResult: {passed}/{len(TESTS)} correct tool choices")