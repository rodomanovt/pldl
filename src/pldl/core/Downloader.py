import os
from yt_dlp import YoutubeDL # type: ignore

class Downloader:

    @staticmethod # throws error
    def download_audio(url: str, work_dir: str, smart_naming: bool = False): # TODO: add formatter and smart file naming
        if not os.path.exists(work_dir):
            print(f"path {work_dir} does not exist")
            return

        ydl_opts = {
            'logger': QuietLogger(),
            'outtmpl': os.path.join(work_dir, '%(title)s.%(ext)s'),
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
            'no_warnings': False,
            'ignoreerrors': False,
        }


        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url.strip()])
            # print("Download successful")


class QuietLogger: # disables log spam in console
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg): # outputs only errors
        print(f"yt-dlp error: {msg}")