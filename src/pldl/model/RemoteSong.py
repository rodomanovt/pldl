class RemoteSong:
    def __init__(self, channel: str, name: str, url: str):
        self.channel = channel
        self.name = name
        self.url = url
        self.artist = channel # changes when smart naming is appled
        self.title = name # changes when smart naming is appled

    def __repr__(self):
        return f"Remote song {self.channel} - {self.name}; url: {self.url}"