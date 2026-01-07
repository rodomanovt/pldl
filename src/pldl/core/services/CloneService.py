import os
from yt_dlp import YoutubeDL
from pldl.core import Downloader, MusicRepository
from pldl.model import RemoteSong


class CloneService:
    def clone(self, url: str, target_dir: str, smart_naming: bool):
        # Определяем, это трек или плейлист
        info = self._get_info(url)
        
        if info.get('_type') == 'playlist':
            print(f"Downloading playlist {info.get('title', 'Unknown')}...")
            self._download_playlist(info, target_dir, smart_naming)
        else:
            print(f"Downloading track {info.get('title', 'Unknown')}...")
            self._download_track(url, info, target_dir, smart_naming)


    def _get_info(self, url: str):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'ignoreerrors': False,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            quit()


    def _download_playlist(self, playlist_info, target_dir: str, smart_naming: bool):
        playlist_dir = target_dir + "/" + playlist_info['title']
        if not os.path.exists(playlist_dir):
            os.mkdir(playlist_dir)

        cnt = 1
        total = len(playlist_info['entries'])
        print(f"Found {total} songs in playlist {playlist_info['title']}")
        for entry in playlist_info['entries']:
            if entry:
                song = RemoteSong(
                    name=entry.get('title', 'Unknown'),
                    url=entry.get('url') or f"https://youtu.be/{entry['id']}",
                    channel=entry.get('channel', entry.get('uploader', 'Unknown'))
                )
                try:
                    Downloader.download_audio(song, playlist_dir, smart_naming)
                    print(f"[{cnt}/{total}] Downloaded {song.artist} - {song.title}")
                    cnt += 1
                except Exception as e:
                    print(e)
                    break


    def _download_track(self, url, video_info, target_dir: str, smart_naming: bool):
        song = RemoteSong(
            name=video_info.get('title', 'Unknown'),
            channel=video_info.get('channel', video_info.get('uploader', 'Unknown')),
            url=url
        )
        try:
            Downloader.download_audio(song, target_dir, smart_naming)
        except Exception as e:
            print(f"Failed to download {song.artist} - {song.title}")