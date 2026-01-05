from pldl.core import Config
import os

class CdService:

    def __init__(self, config: Config):
        self.config = config


    def change_dir(self, new_dir: str):
        if os.path.exists(new_dir):
            self.config.set_music_dir_setting(new_dir)
            return f"Music library path changed to {new_dir}"
        else:
            return f"Path {new_dir} does not exist"