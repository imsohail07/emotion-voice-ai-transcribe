import os
from pydub import AudioSegment

def ensure_wav(input_path: str) -> str:
	ext = os.path.splitext(input_path)[1].lower()

	if ext == ".wav":
		return input_path

	wav_path = os.path.splitext(input_path)[0] + ".wav"

	audio = AudioSegment.from_file(input_path)
	audio = audio.set_channels(1).set_frame_rate(16000)
	audio.export(wav_path, format="wav")

	return wav_path
