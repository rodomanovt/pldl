from pldl.model.Playlist import *
from pldl.model.RemoteSong import *
from pldl.Config import *
from yt_dlp import YoutubeDL # type: ignore
import os

class MusicRepository:

    @staticmethod
    def get_remote_songs_from_playlist(playlist) -> list['RemoteSong']:
        ydl_opts = {
            'extract_flat': True,   # Получаем только базовую информацию (ID, title, url)
            'quiet': True,          # Без лишнего вывода
            'skip_download': True,  # Ничего не скачиваем
            'ignoreerrors': True,   # Пропускать недоступные видео
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist.url.strip(), download=False)
            
            # info — это dict с ключом 'entries', содержащим список видео
            entries = info.get('entries', [])
            
            remote_songs = []
            for entry in entries:
                if entry:  # Некоторые записи могут быть None, если видео недоступно
                    title = entry.get('title', 'Unknown Title')
                    url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                    remote_songs.append(RemoteSong(title=title, url=url))
            
            return remote_songs

        except Exception as e:
            print(f"Failed to fetch playlist: {e}")
            return []



    @staticmethod
    def get_local_song_names_from_playlist(playlist: Playlist) -> list[str]:
        work_dir = Config.get_instance().get_music_dir_setting() + "/" + playlist.name
        if os.path.exists(work_dir):
            result = os.listdir(work_dir)
            return result

        else:
            print(f"Path {work_dir} does not exist")