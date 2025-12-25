class Playlist:
        def __init__(self, name, url, last_updated):
            self.name = name
            self.url = url
            self.last_updated = last_updated

        def __repr__(self):
            return f"Playlist {self.name}, url = {self.url}, last updated at {self.last_updated}"