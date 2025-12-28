from pldl.core import Config, MusicRepository, Downloader
import os

class PullService:

    def __init__(self, config: Config):
        self.config = config


    def pull(self, playlist_name: str, smart_naming: bool):
        work_dir = self.config.get_music_dir_setting()
        playlists = self.config.get_playlists_db()

        if playlist_name:
            # TODO: implement downloading individual playlists
            pass

        else:
            for playlist in playlists:
                playlist_dir = work_dir + "/" + playlist.name
                if os.path.exists(work_dir):
                    if not os.path.exists(playlist_dir):
                        os.mkdir(playlist_dir)

                    try:
                        songs = MusicRepository.get_songs_to_download(playlist)
                    except Exception as e:
                        print(e)
                        continue

                    total = len(songs)
                    print(f"Found {total} new songs in playlist {playlist.name}")
                    cnt = 1

                    for song in songs:
                        try:
                            Downloader.download_audio(song.url, playlist_dir, smart_naming=smart_naming)
                            print(f"[{cnt}/{len(songs)}] Downloaded {song.title}")
                            cnt += 1;
                        except Exception as e: # TODO: save all song urls that got error while downloading. Exclude them for next pulls
                            total -= 1
                            continue
                    
                    self.config.update_playlist_time_setting(playlist.name)


                else:
                    print("path does not exist")
