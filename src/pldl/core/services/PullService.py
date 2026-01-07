from pldl.core import Config, MusicRepository, Downloader
import os

class PullService:

    def __init__(self, config: Config):
        self.config = config


    def pull(self, playlist_name: str, smart_naming: bool):
        work_dir = self.config.get_music_dir_setting()
        playlists = [] # list of playlists to download

        if playlist_name:
            try:
                playlists.append(self.config.get_playlist(playlist_name))
            except FileNotFoundError:
                print(f'Playlist "{playlist_name}" was not found')

        else:
            playlists = self.config.get_playlists_db()

        if smart_naming: print("Using smart naming")

        for playlist in playlists:
            playlist_dir = work_dir + "/" + playlist.name
            if os.path.exists(work_dir):
                if not os.path.exists(playlist_dir):
                    os.mkdir(playlist_dir)

                try:
                    print(f"Fetching new songs from playlist {playlist.name} ...")
                    songs = MusicRepository.get_songs_to_download(playlist)
                except Exception as e:
                    print(e)
                    continue

                total = len(songs)
                print(f"Found {total} new songs in playlist {playlist.name}")
                cnt = 1

                for song in songs:
                    try:
                        Downloader.download_audio(song, playlist_dir, smart_naming=smart_naming)
                        print(f"[{cnt}/{total}] Downloaded {song.artist} - {song.title}")
                        cnt += 1;
                    except Exception as e:
                        print(e)
                        continue
                        # TODO: Save all song urls that got error while downloading. 
                        # TODO: Exclude them for next pulls or
                        # TODO: try to download from different source video.
                
                self.config.update_playlist_time_setting(playlist.name)


            else:
                print("path does not exist")
