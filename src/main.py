import asyncio

from apple_music_lib import get_apple_music_songs
from config import settings
from helpers import create_spotify_playlist
from models import SpotifyCredentials

# TODO: Add Pydantic for data validation
# TODO: Add way to save songs that failed to be added


async def async_main() -> None:
    # TODO: Get input dynamically (i.e., from user)
    #   - playlist url
    #   - playlist name

    url: str = "https://music.apple.com/us/playlist/gymbro/pl.u-55D6X8qU63EXGbj"
    apple_song_list = await get_apple_music_songs(url=url)
    # apple_song_list: list[dict[str, str]] = read_json("apple_music_songs.json")
    spotify_creds: SpotifyCredentials = SpotifyCredentials(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URI,
    )

    create_spotify_playlist(
        song_list=apple_song_list,
        spotify_creds=spotify_creds,
        playlist_name="GymBro",
    )


def main() -> None:
    if __name__ == "__main__":
        asyncio.run(async_main())


main()
