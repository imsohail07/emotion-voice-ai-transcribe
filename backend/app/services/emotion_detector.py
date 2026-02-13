from app.models.emotion_model import predict_emotions

# Map model labels to our UI labels
LABEL_MAP = {
    "joy": "Happy",
    "sadness": "Sad",
    "anger": "Angry",
    "neutral": "Calm",
    "fear": "Nervous",
    "surprise": "Calm",
    "disgust": "Angry"
}

def detect_emotion_from_text(text: str):
    scores = predict_emotions(text)

    mapped = []
    for item in scores:
        label = item["label"].lower()
        score = float(item["score"])

        mapped_label = LABEL_MAP.get(label, label)

        mapped.append({
            "label": mapped_label,
            "score": score
        })

    # Sort by confidence
    mapped.sort(key=lambda x: x["score"], reverse=True)

    return {
        "top_emotion": mapped[0],
        "all_emotions": mapped
    }
