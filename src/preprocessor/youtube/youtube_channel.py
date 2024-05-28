from typing import List, Optional

from pytube import Channel
from logging import getLogger

logger = getLogger(__name__)


class YoutubeChannel:
    def __init__(self, url):
        self.url = url

    def get_channel_videos(self) -> Optional[List[str]]:
        try:
            channel = Channel(self.url)
            for video in channel.video_urls:
                print(video)

            return channel.videos_url
        except Exception as e:
            logger.error(e)
            return


if __name__ == "__main__":
    # channel = YoutubeChannel("https://www.youtube.com/c/ProgrammingKnowledge/videos")
    # print(channel.get_channel_videos())
    from pytube import Channel

    channel = Channel(
        "https://www.youtube.com/user/NewOnNetflix/videos")
    print(channel.videos_url)