from pldl.core import Config

class StatusService:
    def __init__(self, config: Config):
        self.config = config


    def get_status(self) -> list[str]:
        result = []

        music_dir_setting = self.config.get_music_dir_setting()
        result.append(f"Downloading to directory: {music_dir_setting}\n")

        result.append("Playlists:\n")
        playlists = self.config.get_playlists_db()
        for playlist in playlists:
            result.append(playlist)

        return result


