# PLDL - PLAYLIST DOWNLOADER    

pldl is a command line tool for managing and automatically downloading playlistst from different music streaming services. 

Credits to [yt-dlp](https://github.com/yt-dlp/yt-dlp).

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

`TODO`

---

# USAGE AND OPTIONS

```
pldl COMMAND [OPTIONS]
```

**Note: all playlists must be publicly visible or they won't be downloaded**

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