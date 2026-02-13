from transformers import pipeline
from app.core.logger import get_logger

logger = get_logger()

logger.info("Loading emotion detection model...")
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)
logger.info("Emotion model loaded.")

def predict_emotions(text: str):
    if not text or len(text.strip()) == 0:
        return []

    results = emotion_pipeline(text[:512])  # limit length
    return results[0]
