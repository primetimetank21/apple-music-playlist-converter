import asyncio

from apple_music_lib import get_apple_music_songs
from core import models, settings
from helpers import create_cli_parser, create_spotify_playlist

# TODO: Add Pydantic for data validation
# TODO: Add way to save songs that failed to be added


async def async_main() -> None:
    parser = create_cli_parser()
    args = models.CLIArgs(**parser.parse_args().__dict__)

    url: str = args.apple_playlist_url
    apple_song_list = await get_apple_music_songs(url=url)
    spotify_creds = models.SpotifyCredentials(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URI,
    )

    create_spotify_playlist(
        song_list=apple_song_list,
        spotify_creds=spotify_creds,
        playlist_name=args.spotify_playlist_name,
        description=args.playlist_description,
    )


def main() -> None:
    if __name__ == "__main__":
        asyncio.run(async_main())


main()
