from typing import Optional, Dict, List
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from logging import getLogger

logger = getLogger(__name__)


class YoutubeTranscription:
    def __init__(self, url: str, language: str):
        self.url = url
        self.language = language

    @staticmethod
    def get_youtube_video_id(url: str) -> Optional[str]:
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]

        logger.error("Invalid YouTube URL")
        return None

    @staticmethod
    def map_languages_to_code(language: str) -> str:
        """
        Maps human-readable language names to their corresponding language codes.

        Args:
            language (str): The human-readable language name.

        Returns:
            str: The corresponding language code.
        """
        mapper = {
            "Danish": "da",
            "Czech": "cs",
            "Dutch": "nl",
            "English": "en",
            "German": "de",
            "French": "fr",
            "Italian": "it",
            "Japanese": "ja",
            "Korean": "ko",
            "Polish": "pl",
            "Spanish": "es",
        }
        return mapper[language]

    def fetch_transcription(self, video_id: str) -> Optional[List[Dict[str, float | str]]]:
        """
        Fetches the audio of the YouTube video in the specified language.

        Args:
            video_id (str): YouTube video id

        """
        text = None
        generated, manually = None, None

        try:
            logger.info(f"Fetching transcript for video {video_id}")
            transcription_list = YouTubeTranscriptApi.list_transcripts(video_id)

            if not transcription_list:
                logger.info(f"Transcripts disabled for video {video_id}")
                return text

            for transcript in transcription_list:
                if self.language in transcript.language:
                    if transcript.is_generated:
                        generated = transcript
                    else:
                        manually = transcript

            if not generated and not manually:
                lang_code = self.map_languages_to_code(self.language)

                for transcript in transcription_list:
                    translation_languages = transcript.translation_languages

                    for lang in translation_languages:
                        if self.language in lang.get("language"):
                            generated = transcript.translate(lang_code)

            if generated and manually:
                text = manually.fetch()

            elif generated:
                text = generated.fetch()

        except TranscriptsDisabled:
            logger.info(f"Transcripts disabled for video {video_id}")
            return text

        except Exception as e:
            logger.error(f"Error fetching transcript for video {video_id}: {e}")
            return text

        return text

    def get_youtube_transcription(self) -> Optional[str]:
        video_id = self.get_youtube_video_id(self.url)
        logger.info(f"Video ID: {video_id}")

        fetched_transcript = self.fetch_transcription(video_id)

        transcription = ""

        if not fetched_transcript:
            return transcription

        for text in fetched_transcript:
            transcription += text.get("text") + " "

        return transcription

