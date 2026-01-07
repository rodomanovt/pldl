from pldl.model.Playlist import *
from pldl.model.RemoteSong import *
from pldl.core.Config import *
from yt_dlp import YoutubeDL
from mutagen.id3 import ID3
from pathlib import  Path
import os


class MusicRepository:

    @staticmethod
    def get_remote_songs_from_playlist(playlist: Playlist) -> list['RemoteSong']: # raises Exception
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True
        }


        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist.url.strip(), download=False)
        
        # info — это dict с ключом 'entries', содержащим список видео
        entries = info.get('entries', [])
        
        remote_songs = []
        for entry in entries:
            if entry:  # Некоторые записи могут быть None, если видео недоступно
                channel = entry.get('channel', "Unknown artist")
                name = entry.get('title', 'Unknown Title')
                url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                remote_songs.append(RemoteSong(channel, name, url=url))
        
        return remote_songs


    @staticmethod
    def get_local_song_names_from_playlist(playlist: Playlist, paths=False) -> list[str]:
        """Get all mp3 file names or paths in playlist"""
        config = Config.get_instance()
        work_dir = os.path.join(config.get_music_dir_setting(), playlist.name)
        
        if not os.path.exists(work_dir):
            return []

        mp3_names = [
            f for f in os.listdir(work_dir)
            if Path(f).suffix.lower() == ".mp3"
        ]
        
        if paths:
            return [os.path.join(work_dir, f) for f in mp3_names]
        else:
            return mp3_names
        

    @staticmethod
    def get_all_downloaded_urls(paths: list[str]) -> set[str]:
        """Extracts urls from files' metadata"""
        result = set()

        for path in paths:
            if os.path.isfile(path):

                try:
                    tags = ID3(path)
                    frames = tags.getall("TXXX")
                except Exception as e:
                    print(e)

                for frame in frames:
                    if frame.desc == "purl" and frame.text:
                        url = str(frame.text[0]).strip().replace("www.", "").replace("music.", "")
                        result.add(url)

            else:
                print(f"File {path} does not exist")

        return result


    @staticmethod
    def is_downloaded(target_url: str, downloaded_urls: list[str]) -> bool:
        target_url = target_url.replace("www.", "").replace("music.", "")

        return target_url in downloaded_urls
    

    @staticmethod
    def get_songs_to_download(playlist: Playlist) -> list[RemoteSong]: # raises Exeption
        all_remote_songs = MusicRepository.get_remote_songs_from_playlist(playlist)
        all_local_song_paths = MusicRepository.get_local_song_names_from_playlist(playlist, paths=True)
        all_downloaded_urls = MusicRepository.get_all_downloaded_urls(all_local_song_paths)

        result = []
        for song in all_remote_songs:
            if not MusicRepository.is_downloaded(song.url, all_downloaded_urls):
                result.append(song)

        return result