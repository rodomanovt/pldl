import json
import threading
import time
import os
from pldl.model.Playlist import *


class Config:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance


    def __init__(self):
        if not self._initialized:
            self._initialized = True
            config_dir = os.path.dirname(os.path.abspath(__file__))
            self._config_path = os.path.join(config_dir, "config.json")

            with open(self._config_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)


    @classmethod
    def get_instance(cls) -> "Config":
        """Use this to return config instance"""
        return cls()
    

    def save(self) -> None:
        """writes config to json file"""
        with open(self._config_path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)


    def _playlist_exists(self, name: str) -> bool:
        for i in range(len(self._data["playlists"])):
            if self._data["playlists"][i]["name"] == name:
                return True
        return False


    def get_update_on_start_setting(self) -> bool:
        return self._data["settings"]["update_on_start"]


    def get_music_dir_setting(self) -> str:
        return self._data["settings"]["music_dir"]


    def set_update_on_start_setting(self, update_on_start: bool) -> None:
        self._data["settings"]["update_on_start"] = update_on_start
        self.save()


    def set_music_dir_setting(self, music_dir: str) -> None:
        self._data["settings"]["music_dir"] = music_dir
        self.save()


    def get_playlists_db(self) -> list[Playlist]:
        playlists = []
        for el in self._data["playlists"]:
            playlists.append(Playlist(el["name"], el["url"], el["last_updated"]))
        return playlists


    def add_playlist_to_db(self, name: str, url: str) -> None:
        if not self._playlist_exists(name):
            self._data["playlists"].append({"name": name, "url": url, "last_updated": ""})
            self.save()
        else:
            print(f'Playlist "{name}" already exists')


    def remove_playlist_from_db(self, name: str) -> None:
        for i in range(len(self._data["playlists"])):
            if self._data["playlists"][i]["name"] == name:
                self._data["playlists"].pop(i)
                self.save()
                return
            
        print(f'Playlist "{name}" was not found')


    def update_playlist_time_setting(self, name: str) -> None:
        for i in range(len(self._data["playlists"])):
            playlist = self._data["playlists"][i]
            if playlist["name"] == name:
                timestamp = time.localtime()
                time_string = f"{timestamp.tm_mday}.{timestamp.tm_mon}.{timestamp.tm_year} {timestamp.tm_hour}:{str(timestamp.tm_min).zfill(2)}"

                playlist["last_updated"] = time_string
                self.save()
                return
            
        print(f'Playlist "{name}" was not found')
