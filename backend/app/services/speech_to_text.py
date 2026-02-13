import whisper
from app.core.logger import get_logger

logger = get_logger()

# Load model ONCE at startup (important!)
logger.info("Loading Whisper model...")
model = whisper.load_model("base")  # you can change to "small" later
logger.info("Whisper model loaded.")

def transcribe_audio(wav_path: str) -> str:
    logger.info(f"Transcribing: {wav_path}")
    result = model.transcribe(wav_path)
    text = result.get("text", "").strip()
    return text
