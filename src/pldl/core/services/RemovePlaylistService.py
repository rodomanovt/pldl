from pldl.core import Config


class RemovePlaylistService:
    def __init__(self, config: Config):
        self.config = config

    
    def remove_playlist(self, name: str):
        try:
            self.config.remove_playlist_from_db(name)
            return "Playlist removed."
        except FileNotFoundError as e:
            return f'Playlist "{name}" was not found.'