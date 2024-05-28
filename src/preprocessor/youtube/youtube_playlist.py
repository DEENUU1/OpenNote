from typing import List, Optional

from pytube import Playlist
from logging import getLogger

logger = getLogger(__name__)


class YoutubePlaylist:
    def __init__(self, url):
        self.url = url

    def get_playlist_videos(self) -> Optional[List[str]]:
        try:
            playlist = Playlist(self.url)
            urls = []
            for video in playlist.videos:
                urls.append(video.watch_url)

            return urls
        except Exception as e:
            logger.error(e)
            return
