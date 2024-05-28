import os
from typing import Optional

import whisper
from pydub import AudioSegment

from config.settings import settings
from utils.get_date_hash import get_date_hash
from logging import getLogger

logger = getLogger(__name__)


class AudioTranscription:
    def __init__(self, audio_file_path: str, whisper_model: str, chunk_size: int = 150):
        self.audio_file_path = audio_file_path
        self.whisper_model = whisper_model
        self.chunk_size = chunk_size

    @staticmethod
    def numerical_sort(chunk) -> int:
        return int(chunk.split('_')[1].split('.')[0])

    def split_audio_to_chunks(self) -> Optional[str]:
        try:
            logger.info(f"Splitting audio file {self.audio_file_path} into chunks")
            audio = AudioSegment.from_file(self.audio_file_path)

            chunk_length = self.chunk_size * 1000
            chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
            logger.info(f"Audio file split into {len(chunks)} chunks")

            date_hash = get_date_hash()
            output_directory = f"{settings.AUDIO_CHUNK_FILE_PATH}{date_hash}"
            os.makedirs(output_directory, exist_ok=True)

            for i, chunk in enumerate(chunks):
                chunk.export(os.path.join(output_directory, f"chunk_{i}.mp3"), format="mp3")
                logger.info(f"Chunk {i} exported to {output_directory}")

            return output_directory

        except Exception as e:
            print(f"Error while splitting audio file {self.audio_file_path}: {e}")
            return

    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        model = whisper.load_model(self.whisper_model)

        try:
            result = model.transcribe(audio_path)
            return result.get("text")
        except Exception as e:
            print(f"Error while transcribing audio file {audio_path}: {e}")
            return

    def run(self) -> Optional[str]:
        result = ""

        audio_path = self.split_audio_to_chunks()
        if not audio_path:
            return None

        sorted_chunks = sorted(os.listdir(audio_path), key=self.numerical_sort)
        for chunk in sorted_chunks:
            chunk_path = f"{audio_path}/{chunk}"
            transcription = self.transcribe_audio(chunk_path)
            if not transcription:
                continue
            result += transcription
            logger.info(f"Transcribed chunk {chunk}")
            # os.remove(chunk_path)
            # print(f"Removed chunk {chunk}")

        return result
