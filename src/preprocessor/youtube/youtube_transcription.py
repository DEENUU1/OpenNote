from typing import Optional
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled


class YoutubeTranscription:
    def __init__(self, url: str):
        self.url = url

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

        print("Couldn't find video id for the given url")
        return None

    def get_youtube_transcription(self) -> Optional[str]:
        video_id = self.get_youtube_video_id(self.url)
        print(f"Youtube video id: {video_id}")

        try:
            transcription_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except TranscriptsDisabled:
            return

        fetched_transcription = None

        try:
            transcript = transcription_list.find_manually_created_transcript(["en", "pl"])
            fetched_transcription = transcript.fetch()

        except NoTranscriptFound:
            pass

        try:
            transcript = transcription_list.find_generated_transcript(["en", "pl"])
            fetched_transcription = transcript.fetch()

        except NoTranscriptFound:
            pass

        if not fetched_transcription:
            return None

        transcription = ""

        for text in fetched_transcription:
            transcription += text.get("text") + " "

        return transcription

