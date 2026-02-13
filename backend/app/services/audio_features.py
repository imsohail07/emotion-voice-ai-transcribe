import librosa
import numpy as np

def extract_audio_features(wav_path: str):
    y, sr = librosa.load(wav_path, sr=16000)

    duration = librosa.get_duration(y=y, sr=sr)

    # Energy
    rms = np.mean(librosa.feature.rms(y=y))

    # Silence ratio
    intervals = librosa.effects.split(y, top_db=25)
    voiced_duration = sum((end - start) for start, end in intervals) / sr
    silence_ratio = 1 - (voiced_duration / duration)

    # Tempo (speech rate proxy)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    return {
        "duration": float(duration),
        "rms": float(rms),
        "silence_ratio": float(silence_ratio),
        "tempo": float(tempo)
    }
