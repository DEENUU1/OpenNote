from pytube import YouTube
import os
from config.settings import settings
from typing import Optional
from logging import getLogger

logger = getLogger(__name__)


class YoutubeDownloader:
    def __init__(self, url: str):
        self.url = url

    def download(self) -> Optional[str]:
        try:
            logger.info(f"Downloading Youtube video from {self.url}")
            youtube = YouTube(self.url)
            audio_download = youtube.streams.filter(only_audio=True).first()
            out_file = audio_download.download(output_path=settings.YOUTUBE_FILE_PATH)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            logger.info(f"Youtube video downloaded from {self.url}")
            return new_file
        except Exception as e:
            logger.error(f"Error while downloading Youtube video from {self.url}: {e}")
            return
