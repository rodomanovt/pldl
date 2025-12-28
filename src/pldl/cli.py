from pldl.core.Config import Config
from pldl.core.services import *
from pldl import __version__
import typer
from typing import Optional
from urllib.parse import urlparse


def validate_url(url: str) -> str:
    """Check if url looks like yt music"""
    if not url:
        raise typer.BadParameter("URL cannot be empty")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or "youtube.com" not in parsed.netloc:
        raise typer.BadParameter("URL must be a YouTube Music playlist")
    return url


app = typer.Typer(help="CLI tool to download youtube music playlists")


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
        help="Enable smart file naming (e.g., 'Artist - Title')",
        is_flag=True,
    )
) -> None:
    """Auto download all new tracks. 
    If playlist_name specified, download new tracks only from this playlist"""
    typer.echo(playlist_name)
    typer.echo(smart_naming)
    pass


@app.command()
def clone(
    playlist_url: str = typer.Argument(..., help="Youtube music playlist url"),
    smart_naming: bool = typer.Option(False,
        "-s", "--smart-naming",
        help="Enable smart file naming (e.g., 'Artist - Title')",
        is_flag=True,
    )
) -> None:
    """Downloads all tracks from youtube playlist to your working directory"""
    typer.echo(playlist_url)
    typer.echo(smart_naming)
    pass


@app.command()
def cd(
    new_work_dir: str = typer.Argument(..., help = "New work directory")
) -> None:
    """Change where your playlists are going to be saved"""
    typer.echo(new_work_dir)
    pass


if __name__ == "__main__":
    app()