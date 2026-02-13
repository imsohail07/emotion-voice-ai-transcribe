import subprocess
import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")
TEMP_DIR = Path("temp")

UPLOAD_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

def save_upload_file(upload_file) -> Path:
    ext = Path(upload_file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())

    return file_path

def convert_to_wav(input_path: Path) -> Path:
    output_path = TEMP_DIR / f"{input_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-ar", "16000",
        "-ac", "1",
        str(output_path)
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    return output_path
