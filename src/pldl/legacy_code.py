import googleapiclient.discovery
from pytube import YouTube, Search
import os
import ffmpeg
from typing import Any


developer_key = ""
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name,api_version,developerKey=developer_key)


class Video:
    def __init__(self, url:str, title:str):
        self.url: str = url
        self.song: YouTube = YouTube(url)
        self.title: str = formatted(title)

    def download_audio(self, path:str) -> None:
        try:
            self.song.streams.filter(adaptive=True, only_audio=True, file_extension='mp4').order_by('abr')[0].download(output_path=path)
            os.rename(f'{path}/{self.song.streams.first().default_filename}', f'{path}/{self.title}.mp4')
            ffmpeg.input(f'{path}/{self.title}.mp4').output(f'{path}/{self.title}.mp3', loglevel='quiet').run()
            os.remove(f'{path}/{self.title}.mp4')
            print(f'downloaded {self.title}')
        except Exception as error:
            print(f'{type(error).__name__}: {self.title}')


    def download_video(self, path:str) -> None:
        global cnt_successful
        try:
            self.song.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(output_path=path)
            os.rename(f'{path}/{self.song.streams.first().default_filename}', f'{path}/{self.title}.mp4')
        except Exception as error:
            print(f'{type(error).__name__}: {self.title}')


def formatted(filename: str) -> str:
    return filename.replace('.', '').replace('"', '').replace('/', '').replace('|', '')


def results_from_playlist(playlistId:str) -> dict[Any]:
    results = youtube.playlistItems().list(part="snippet",playlistId=playlistId,maxResults='100').execute()
    nextPageToken = results.get('nextPageToken')

    while 'nextPageToken' in results:
        nextPage = youtube.playlistItems().list(part="snippet", playlistId=playlistId, maxResults='50', pageToken=nextPageToken).execute()
        results['items'] = results['items'] + nextPage['items']
        if 'nextPageToken' not in nextPage:
            results.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    return results


def videos_from_results(results: dict) -> list[Video]:
    taken_videos = []

    for result in results['items']:
        try:
            taken_videos.append(Video(url=f'http://youtube.com/watch?v={result['snippet']['resourceId']['videoId']}', title=formatted(result['snippet']['title'])))
        except KeyError:
            print(f'{result['snippet']['title']} got KeyError')

    return taken_videos


def filenames_from_results(results: dict) -> list[str]:
    filenames = []
    for result in results['items']:
        try:
            filenames.append(formatted(result['snippet']['title']))
        except KeyError:
            print(f'{result['snippet']['title']} got KeyError')
    return filenames


def video_by_search(searchword:str) -> Video:
    if 'youtu.be/' in searchword or 'youtube.com/watch' in searchword:
        return Video(url=searchword, title=YouTube(searchword).title)
    else:
        search = Search(searchword)
        videoId: str = search.results[0].video_id
        return Video(url=f'http://youtube.com/watch?v={videoId}', title=searchword)


def get_downloaded_songs(path: str) -> list[str]:
    available_songs = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            available_songs.append(filename[:-4])
        return available_songs


def is_downloaded(song1: str) -> bool:
    downloaded_songs = get_downloaded_songs(path)
    found = False
    song1 = formatted(song1)
    for song2 in downloaded_songs:
        jaccard_similarity = len(set(song1) & set(song2)) / len(set(song1) | set(song2))
        if jaccard_similarity > 0.87:
            found = True
            break
    return found


legkiy_phonk = 'PL752Mo0P5AdgYBs7ipz8hjalr86CuZifq'
heavy_phonk = 'PL752Mo0P5AdhLmcnFlRzFeQqC-OSNZchD'
dikiy_bass = 'PL752Mo0P5AdiwyHgW9Qs4rm3MyIn1L9B8'


if __name__ == '__main__':
    function: str = 'update_playlist'
    path: str = 'E:/audios/Лёгкий фонк'
    searchword: str = 'swerve wig split'
    cnt_successful: int = 0

    if function == 'download_playlist':
        results: dict = results_from_playlist(dikiy_bass)
        videos: list = videos_from_results(results)
        test_slice = slice(None, 3, None)
        for vid in videos[test_slice]:
            vid.download_audio(path)
            cnt_successful += 1
            print(f'{cnt_successful}/{len(videos[test_slice])}')

    elif function == 'search':
        video_by_search(searchword).download_audio(path)

    elif function == 'update_playlist':
        results: dict = results_from_playlist(legkiy_phonk)
        videos = videos_from_results(results)
        for filename in filenames_from_results(results):
            if not is_downloaded(filename):
                for i in range(len(videos)-1, -1, -1):
                    if videos[i].name == filename:
                        videos[i].download_audio(path)
                        break