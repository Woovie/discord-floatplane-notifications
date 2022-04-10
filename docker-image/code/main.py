"""
Not a module :^)
"""
from asyncio import sleep
from json import loads as jsonloads
import requests
import discord
import configloader
from videohistory import VideoHistoryLocal

def main():
    """
    Program instantiation via CLI
    """
    discord_client = DiscordClient()
    try:
        discord_client.config
    finally:
        discord_client.run(discord_client.config.discord.token)


class APICaller():
    """
    Handles API calls to Floatplane API
    """
    def __init__(self):
        self.videos = []

    def process_api_results(self, api_endpoint: str, channel_id: str, limit: int, video_url: str):
        """
        Instantiates API call method, loads in returned data, parses and reshapes into a format of
        my own choosing to pass to other methods in the stack
        """
        apiresponse = jsonloads(self.check_for_videos(api_endpoint, channel_id, limit))
        for video in apiresponse:
            self.videos.append({
                "id": video['id'],
                "title": video['title'],
                "url": f"{video_url}{video['id']}",
                "image": video['thumbnail']['path']
            })

    @staticmethod
    def check_for_videos(api_endpoint: str, channel_id: str, limit: int):
        """
        Does a simple GET request to an open API on Floatplane
        Retreives the last 20 uploaded videos
        """
        api = f"{api_endpoint}{channel_id}&limit={limit}"
        result = requests.get(api)
        return result.text

class DiscordClient(discord.Client):
    """
    Discord wrapper class
    Adds some new methods, overwrites others
    """

    def __init__(self):
        discord.Client.__init__(self)
        self.config =  configloader.Configuration(
            configuration_type="ini"
        )
        self.history = VideoHistoryLocal()
        # TODO Add an environment detection (Azure, AWS) logic to set which class to use?
        self.api = APICaller()
        self.history.read()

    async def on_ready(self):
        """
        Starts once the rest of the discord.Client has finished instantiation
        """
        await self.get_video_data()
        await self.process_videos()
        await self.close()

    async def get_video_data(self):
        """
        Contains a single method call to APICaller.process_api_results that explodes to many lines
        """
        self.api.process_api_results(
            api_endpoint=self.config.floatplane.api_endpoint,
            limit=self.config.floatplane.limit,
            video_url=self.config.floatplane.video_url,
            channel_id=self.config.floatplane.channel
        )

    async def process_videos(self):
        """
        Reads the data from Floatplane API results and posts if the video is new
        """

        for video in self.api.videos:
            if not self.history[video['id']]:
                await self.post_video(video)

    async def post_video(self, video: dict):# TODO BUILD AN EMBED
        channel = self.get_channel(self.config.discord.channel_id)
        embed = discord.Embed(title=f"New LTT Video - {video['title']}", url=video['url'])
        embed.set_image(url=video['image'])
        await channel.send(embed=embed)
        self.history[video['id']]
        await sleep(5)

if __name__ == "__main__":
    main()
