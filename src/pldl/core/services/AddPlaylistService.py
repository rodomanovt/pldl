from pldl.core import Config, MusicRepository
from pldl.model import Playlist

class AddPlaylistService:
    def __init__(self, config: Config):
        self.config = config

    
    def add_playlist(self, name: str, url: str) -> str:
        if not self._is_playlist_url(name, url):
            return f'Playlist not added: Could not fetch playlist data.\n\
Make sure that the URL is a valid youtube music playlist and the playlist is public.' 

        try:
            self.config.add_playlist_to_db(name, url)
            return "Playlist added."
        except FileExistsError:
            return f'Playlist not added: Playlist "{name}" already exists.'
        

    def _is_playlist_url(self, _: str, url: str) -> bool:
        """check if url is public youtube music playlist"""
        try:
            MusicRepository.get_remote_songs_from_playlist(Playlist(_, url))
            return True
        except Exception as e:
            return False