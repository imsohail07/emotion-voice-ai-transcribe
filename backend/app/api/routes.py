import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.utils.audio_utils import save_upload_file, convert_to_wav
from app.services.speech_to_text import transcribe_audio
from app.services.emotion_detector import detect_emotion_from_text
from app.services.confidence_estimator import estimate_confidence
from app.services.emotion_service import analyze_emotion_timeline

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Emotion Voice AI backend running"
    }


@router.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".wav", ".mp3", ".m4a", ".webm", ".ogg")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        # 1️⃣ Save uploaded file
        saved_path = save_upload_file(file)

        # 2️⃣ Convert to WAV
        wav_path = convert_to_wav(saved_path)

        # 3️⃣ Transcribe
        transcript = transcribe_audio(str(wav_path))

        # 4️⃣ Global emotion (text-based)
        emotion_result = detect_emotion_from_text(transcript)

        # 5️⃣ Confidence
        confidence_result = estimate_confidence(str(wav_path), transcript)

        # 6️⃣ Emotion timeline (audio-based)
        timeline = analyze_emotion_timeline(str(wav_path))

        # 7️⃣ Return everything
        return {
            "status": "success",
            "transcript": transcript,
            "emotion": emotion_result,
            "confidence": confidence_result,
            "emotion_timeline": timeline
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
