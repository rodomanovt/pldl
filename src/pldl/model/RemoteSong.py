class RemoteSong:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def __repr__(self):
        return f"Remote song {self.title}, url: {self.url}"