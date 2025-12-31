import os
from yt_dlp import YoutubeDL # type: ignore
from pldl.model import RemoteSong
from pldl.core.Formatter import *


class Downloader:

    @staticmethod # throws error
    def download_audio(song: RemoteSong, work_dir: str, smart_naming = False): # TODO: add formatter and smart file naming
        if not os.path.exists(work_dir):
            print(f"path {work_dir} does not exist")
            return
        
        if smart_naming:
            artist, title = get_smart_song_name(song.channel, song.name)
            song.artist = artist
            song.title = title
            filename = f"{artist} - {title}.%(ext)s"
            outtmpl = os.path.join(work_dir, filename)
        else:
            outtmpl = os.path.join(work_dir, '%(title)s.%(ext)s'),
        
        ydl_opts = {
            'logger': QuietLogger(),
            'outtmpl': outtmpl,
            'format': 'bestaudio/best',
            'no_warnings': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail',  # ← встраивает обложку в MP3
                },
                {
                    'key': 'FFmpegMetadata',   # ← опционально: сохраняет другие метаданные
                }
            ],
            'writethumbnail': True,       # ← обязательно: скачивает thumbnail
            'quiet': False,
            'ignoreerrors': False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([song.url.strip()])


class QuietLogger: # disables log spam in console
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg): # outputs only errors
        print(f"yt-dlp error: {msg}")