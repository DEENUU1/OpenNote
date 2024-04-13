import os
from typing import Optional

import whisper
from pydub import AudioSegment

from config.settings import settings
from utils.get_date_hash import get_date_hash


class AudioTranscription:
    def __init__(self, audio_file_path: str, whisper_model: str, chunk_size: int = 150):
        self.audio_file_path = audio_file_path
        self.whisper_model = whisper_model
        self.chunk_size = chunk_size

    def split_audio_to_chunks(self) -> Optional[str]:
        try:
            audio = AudioSegment.from_file(self.audio_file_path)

            chunk_length = self.chunk_size * 1000
            chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
            print(f"Split file into {len(chunks)} chunks")

            date_hash = get_date_hash()
            output_directory = f"{settings.AUDIO_CHUNK_FILE_PATH}{date_hash}"
            os.makedirs(output_directory, exist_ok=True)

            for i, chunk in enumerate(chunks):
                chunk.export(os.path.join(output_directory, f"chunk_{i}.mp3"), format="mp3")
                print(f"Chunk {i} exported")

            return output_directory

        except Exception as e:
            print(f"Error while splitting audio file: {e}")
            return

    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        model = whisper.load_model(self.whisper_model)

        try:
            result = model.transcribe(audio_path)
            return result.get("text")
        except Exception as e:
            print(f"Error while transcribing {audio_path}: {e}")
            return

    def run(self) -> Optional[str]:
        result = ""

        audio_path = self.split_audio_to_chunks()
        if not audio_path:
            return None
        for chunk in os.listdir(audio_path):
            chunk_path = f"{audio_path}/{chunk}"
            transcription = self.transcribe_audio(chunk_path)
            if not transcription:
                continue
            result += transcription
            print(f"Transcribed chunk {chunk}")
            # os.remove(chunk_path)
            # print(f"Removed chunk {chunk}")

        return result
