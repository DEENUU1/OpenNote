from pytube import YouTube
import os
from config.settings import settings
from typing import Optional


class YoutubeDownloader:
    def __init__(self, url: str):
        self.url = url

    def download(self) -> Optional[str]:
        try:
            youtube = YouTube(self.url)
            audio_download = youtube.streams.filter(only_audio=True).first()
            out_file = audio_download.download(output_path=settings.YOUTUBE_FILE_PATH)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            return new_file
        except Exception as e:
            print(f"Error while downloading Youtube video: {e}")
            return
