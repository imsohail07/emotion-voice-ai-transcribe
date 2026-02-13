import re
from app.services.audio_features import extract_audio_features

FILLER_WORDS = ["uh", "um", "like", "you know", "actually", "basically"]

def count_fillers(text: str):
    text = text.lower()
    count = 0
    for w in FILLER_WORDS:
        count += len(re.findall(rf"\b{w}\b", text))
    return count

def estimate_confidence(wav_path: str, transcript: str):
    features = extract_audio_features(wav_path)

    duration = features["duration"]
    rms = features["rms"]
    silence_ratio = features["silence_ratio"]
    tempo = features["tempo"]

    word_count = len(transcript.split())
    fillers = count_fillers(transcript)

    # Speech rate (words per second)
    wps = word_count / max(duration, 1)

    # --- Scoring heuristics ---
    score = 50.0  # base

    # Energy
    if rms > 0.05:
        score += 10
    else:
        score -= 10

    # Silence penalty
    score -= silence_ratio * 30

    # Speech rate bonus
    if 1.5 <= wps <= 3.5:
        score += 10
    else:
        score -= 10

    # Filler penalty
    score -= fillers * 2

    # Clamp
    score = max(0, min(100, score))

    # Level
    if score >= 75:
        level = "High"
    elif score >= 50:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": round(score, 2),
        "level": level,
        "metrics": {
            "duration": duration,
            "words_per_sec": round(wps, 2),
            "silence_ratio": round(silence_ratio, 3),
            "energy": round(rms, 5),
            "fillers": fillers
        }
    }
