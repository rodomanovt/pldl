from pldl.Downloader import *
from pldl.Config import *
from pldl.MusicRepository import *


def main():
    # Downloader.download_audio("https://music.youtube.com/watch?v=ijRO-GzfJzY", "/media/timofey/New Volume/Music/Synthwave")
    config = Config.get_instance()
    for el in config.get_playlists_db():
        songs = MusicRepository.get_remote_songs_from_playlist(el)
        print(*songs, sep='\n')
        break
        



if __name__ == "__main__":
    main()