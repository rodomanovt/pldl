from pldl.core.Downloader import *
from pldl.core.Config import *
from pldl.core.MusicRepository import *


def main():
    # Downloader.download_audio("https://music.youtube.com/watch?v=ijRO-GzfJzY", "/media/timofey/New Volume/Music/Synthwave")
    # Downloader.download_audio("https://music.youtube.com/watch?v=d2vICCLlS_c", "/media/timofey/New Volume/Music/Synthwave")
    config = Config.get_instance()
    # for el in config.get_playlists_db():
    #     songs = MusicRepository.get_remote_songs_from_playlist(el)
    #     print(*songs, sep='\n')
    #     break
    print(MusicRepository.is_downloaded(config.get_playlists_db()[0], "https://youtube.com/watch?v=d2vICCLlS_c"))
        



if __name__ == "__main__":
    main()