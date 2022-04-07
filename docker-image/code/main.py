from asyncio import sleep
import configparser, json, requests, discord

def main():
    instance.process_video_results()
    discordclient = DiscordClient()
    discordclient.run(config['discord']['token'])


class APICaller():
    def __init__(self):
        self.videos = []
        pass

    def process_video_results(self):
        apiresponse = json.loads(self.check_for_videos())
        for video in apiresponse:
            self.videos.append({
                "id": video['id'],
                "title": video['title'],
                "url": f"{config['floatplane']['videourl']}{video['id']}",
                "image": video['thumbnail']['path']
            })

    @staticmethod
    def check_for_videos():
        api = f"{config['floatplane']['apiendpoint']}{config['floatplane']['channel']}&limit={config['floatplane']['limit']}"
        result = requests.get(api)
        return result.text


class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        # Add some form of storage and checking here... JSON file?
        self.history = VideoHistoryLocal()
        self.history.read()
        await self.process_videos()
        await self.close()
    
    async def process_videos(self):
        if len(self.history) == 0:
            instance.videos.reverse()# We need to inverse so we get the videos in order of release, so the latest is the latest post
        for video in instance.videos:
            if not self.history[video['id']]:
                await self.post_video(video)

    async def post_video(self, video: dict):# TODO BUILD AN EMBED
        channel = self.get_channel(int(config['discord']['channelid']))
        embed = discord.Embed(title=f"New LTT Video - {video['title']}", url=video['url'])
        embed.set_image(url=video['image'])
        await channel.send(embed=embed)
        self.history[video['id']] = True
        await sleep(5)


class VideoHistoryLocal:
    def __init__(self):
        self.history = []

    def __getitem__(self, videoid: str):
        return videoid in self.history

    def __setitem__(self, videoid: str, sent: bool):
        self.history.append(videoid)
        self.save()

    def __len__(self):
        return len(self.history)

    def read(self, filename: str = 'history.json'):
        with open(filename, 'r') as historydata:
            self.history = json.load(historydata)

    def save(self, filename: str = 'history.json'):
        with open(filename, 'w') as historydata:
            json.dump(self.history, historydata)

instance = APICaller()

if __name__ == "__main__":
    main()
