from pldl.core.Config import Config
from pldl.core.services import *
from pldl import __version__
import typer
from typing import Optional
from urllib.parse import urlparse
import os


def validate_url(url: str) -> str:
    """Check if url looks like yt music"""
    if not url:
        raise typer.BadParameter("URL cannot be empty")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or "youtube.com" not in parsed.netloc:
        raise typer.BadParameter("URL must be a YouTube Music playlist")
    return url


app = typer.Typer(help="CLI tool to download youtube music playlists",
                  no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        None,
        "--version",
        help="Show the version and exit.",
        is_flag=True,
    ),
) -> None:
    if version:
        typer.echo(f"pldl version {__version__}")
        raise typer.Exit()


@app.command()
def status() -> None:
    """Show your local playlists and settings"""
    config = Config.get_instance()
    service = StatusService(config)

    status: list[str] = service.get_status()
    for s in status:
        typer.echo(s)


@app.command()
def add(
    playlist_name: str = typer.Argument(..., help="Local playlist name"),
    playlist_url: str = typer.Argument(..., help="Youtube music playlist url")
) -> None:
    """Add playlist to auto-update list"""
    playlist_url = validate_url(playlist_url)

    config = Config.get_instance()
    service = AddPlaylistService(config)

    typer.echo("Fetching playlist data...")
    response: str = service.add_playlist(playlist_name, playlist_url)
    typer.echo(response)


@app.command()
def remove(
    playlist_name: str = typer.Argument(..., help="Local playlist name")
) -> None:
    """Remove playlist from auto-update list"""
    config = Config.get_instance()
    service = RemovePlaylistService(config)

    response: str = service.remove_playlist(playlist_name)
    typer.echo(response)



@app.command()
def pull(
    playlist_name: Optional[str] = typer.Argument(None, help="Local playlist name"),
    smart_naming: bool = typer.Option(False,
        "-s", "--smart-naming",
        help="Use smart 'Artist - Title.mp3' naming",
        is_flag=True,
    )
) -> None:
    """Auto download all new tracks. 
    If playlist_name specified, download new tracks only from this playlist"""
    config = Config.get_instance()
    service = PullService(config)

    service.pull(playlist_name, smart_naming)



@app.command()
def clone(
    url: str = typer.Argument(..., help="YouTube Music track or playlist URL"),
    smart_naming: bool = typer.Option(
        False,
        "-s", "--smart-naming",
        help="Use smart 'Artist - Title.mp3' naming"
    ),
) -> None:
    """Download a track or playlist into the current directory"""
    current_dir = os.getcwd()
    service = CloneService()
    service.clone(url.strip(), current_dir, smart_naming)



@app.command()
def cd(
    new_work_dir: str = typer.Argument(..., help = "New library directory")
) -> None:
    """Change music library directory, where playlists are downloaded"""
    config = Config.get_instance()
    service = CdService(config)

    response = service.change_dir(new_work_dir)
    typer.echo(response)


if __name__ == "__main__":
    app()