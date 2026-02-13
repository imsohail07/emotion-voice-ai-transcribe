import soundfile as sf
import numpy as np
import os

def split_audio(path: str, segment_seconds=5):
    audio, sr = sf.read(path)
    
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    segment_length = int(segment_seconds * sr)

    segments = []
    for i in range(0, len(audio), segment_length):
        chunk = audio[i:i + segment_length]
        if len(chunk) < segment_length // 2:
            continue

        segments.append(chunk)

    return segments, sr
