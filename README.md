# PLDL - PLAYLIST DOWNLOADER    

**pldl** is a command line tool for managing and automatically downloading playlistst from different music streaming services. 

Credits to [yt-dlp](https://github.com/yt-dlp/yt-dlp).

**Note:** pldl is in alpha, so bugs are expected. Feel free to open an [issue](https://github.com/rodomanovt/pldl/issues/new) and report any problems.

---

# FEATURES

- Currently supported services: `Youtube Music`

- Git-like commands for managing playlists

- Every playlist is downloaded to a separate folder in you music library directory

- Playlist tracking and downloading new songs

- Support for downloading individual playlists and songs

- Smart file naming (`Artist - Title.mp3`). Removes unnecessary words from file names based on video title and publisher channel

---

# INSTALLATION

**IMPORTANT: Make sure that you have [ffmpeg](https://www.ffmpeg.org/) installed, or downloading will not work.** You can check if `ffmpeg` is installed correctly by running
```
ffmpeg -h
```

## Installation using `uv` (windows/linux)

1) Make sure that you have [uv](https://docs.astral.sh/uv/) installed. You can check if `uv` is installed correctly by running
    ```
    uv --verson
    ```

2) Clone this repository to any folder by running
    ```
    git clone https://github.com/rodomanovt/pldl.git
    ```

3) Go to the cloned repo folder and run
    ```
    uv sync
    uv tool install .
    ```

4) On windows: add the path `%USERPROFILE%/.local/bin` to the `Path` environment variable.

5) Check if `pldl` got installed correctly by running
    ```
    pldl --version
    ```
**Tip: you can automatically update yt-dlp library by running `pldl --update-yt-dlp`**

---

# USAGE AND OPTIONS

```
pldl COMMAND [OPTIONS]
```

**IMPORTANT: all playlists must be public or unlisted, otherwise they won't be downloaded.**

## Commands:

- **`status`** - Show the list of tracked playlists and additional info.

- **`add`** - Add playlist to tracking list.
    - **Arguments**:
        ```
        playlist_name       - Name of new playlist
        playlist_url        - URL of the playlist
        ```

- **`remove`** - Remove playlist from tracking list.
    - **Arguments**:
        ```
        playlist_name       - Name of the playlist to remove
        ```

- **`pull`** - Download all new songs from tracked playlists.
    - **Arguments**:
        ```
        playlist_name       - If specified, downloads new songs only from this playlist
        -s, --smart-naming  - If specified, uses smart file naming
        ```

- **`clone`** - Download individual song or playlist to the current directory. Playlist contents are saved in a subfolder.
    - **Arguments**:
        ```
        url                 - URL of the playlist or song to download
        -s, --smart-naming  - If specified, uses smart file naming
        ```

- **`cd`** - Change path to your music library
    - **Arguments**:
        ```
        new_dir             - new path to the music library
        ```