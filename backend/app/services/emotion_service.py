import os
import tempfile
import numpy as np
import soundfile as sf

from app.services.audio_segmenter import split_audio
from app.models.emotion_model import emotion_pipeline
from app.services.speech_to_text import transcribe_audio


def analyze_emotion_timeline(wav_path: str):
    segments = split_audio(wav_path)

    timeline = []

    for i, segment in enumerate(segments):
        # ✅ If split_audio returns (audio, sr)
        if isinstance(segment, tuple) and len(segment) == 2:
            segment, sr = segment
        else:
            sr = 16000

        # ✅ Convert to numpy float32
        segment = np.array(segment, dtype=np.float32)

        # ✅ If 0D (shape=()) skip
        if segment.ndim == 0:
            continue

        # ✅ If 2D, convert to mono safely
        if segment.ndim == 2:
            # (samples, channels) OR (channels, samples)
            if segment.shape[0] < segment.shape[1]:
                segment = segment.mean(axis=0)
            else:
                segment = segment.mean(axis=1)

        # ✅ If more than 2D, flatten
        if segment.ndim > 2:
            segment = segment.flatten()

        # ✅ Force 1D
        segment = segment.reshape(-1)

        # ✅ Skip very tiny / empty segments
        if segment.size < 10:
            continue

        # ✅ Normalize to avoid bad amplitude values
        mx = np.max(np.abs(segment))
        if mx > 0:
            segment = segment / mx

        # ✅ Save as temp wav
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            temp_wav = tmp.name

        # ✅ Force WAV PCM format (ensure 1D mono array for soundfile)
        if segment.ndim == 1:
            segment = segment.reshape(-1, 1)
        sf.write(temp_wav, segment, sr, format="WAV", subtype="PCM_16")

        # ✅ Transcribe
        transcript = transcribe_audio(temp_wav)

        # ✅ Delete temp file
        try:
            os.remove(temp_wav)
        except:
            pass

        # ✅ Emotion from transcript
        if not transcript or transcript.strip() == "":
            label = "neutral"
            score = 1.0
        else:
            out = emotion_pipeline(transcript, top_k=1)

            if isinstance(out, list) and len(out) > 0 and isinstance(out[0], dict):
                label = str(out[0].get("label", "unknown")).lower()
                score = float(out[0].get("score", 0.0))
            else:
                label = "unknown"
                score = 0.0

        timeline.append({
            "segment_index": i,
            "transcript": transcript,
            "label": label,
            "score": score
        })

    return timeline
