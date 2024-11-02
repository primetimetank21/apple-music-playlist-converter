import asyncio
import json
from typing import Any, Dict, List, Union
import logging
from urllib.parse import parse_qs, urlparse
from logger_lib import create_logger
import spotipy  # type: ignore
from spotipy.oauth2 import SpotifyOAuth  # type: ignore
from apple_music_lib.get_apple_music import get_apple_music_songs


def create_spotify_playlist(
    song_list: List[Dict[str, str]],
    spotify_creds: Dict[str, str],
    playlist_name: str,
    scope: Union[str, List[str]] = [
        "user-library-modify",
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-library-modify",
        "user-library-read",
        # "user-read-private"
    ],
    public: bool = False,
    description: str = "Apple Music Playlist converted to Spotify Playlist! :)",
) -> None:
    # Create logger
    # logger = create_logger(name=__name__, level=logging.INFO)
    logger = create_logger(name=__name__, level=logging.DEBUG)

    # Authenticate user
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_creds["client_id"],
            client_secret=spotify_creds["client_secret"],
            redirect_uri=spotify_creds["redirect_url"],
            scope=scope,
        )
    )

    # Get current user info
    current_user: Dict[str, Union[str, Any]] = sp.current_user()

    # Check if playlist already exists
    failed_attempts: int = 0
    FAILED_LIMIT: int = 5
    offset: int = 0
    playlist_id: str = ""

    while (not playlist_id) or (failed_attempts < FAILED_LIMIT):
        try:
            user_playlists_response = sp.user_playlists(
                user=current_user["id"], limit=50, offset=offset
            )
            logger.debug(f"{user_playlists_response=}\n")

            # Get playlist ID if it exists
            for playlist in user_playlists_response["items"]:
                if playlist_name == playlist["name"]:
                    playlist_id = playlist["id"]
                    logger.info(f"Found playlist: '{playlist_name}'")
                    break

            # Create playlist if it doesn't exist
            if playlist_id:
                break

            # Get next offset
            parsed_url = urlparse(user_playlists_response["next"])

            # Get the query parameters
            query_params = parse_qs(parsed_url.query)
            offset = int(query_params["offset"][0])
        except Exception as e:
            logger.exception(e)
            failed_attempts += 1

    # Create playlist if it doesn't exist
    if not playlist_id:
        logger.info(f"Playlist '{playlist_name}' not found. Creating...")
        create_user_playlist_response = sp.user_playlist_create(
            user=current_user["id"],
            name=playlist_name,
            public=public,
            description=description,
        )
        logger.debug(f"{create_user_playlist_response=}\n")
        playlist_id = create_user_playlist_response["id"]
        logger.info(f"Created playlist: '{playlist_name}'")

    # Add songs to playlist
    # TODO


def get_creds() -> Dict[str, str]:
    with open("spotify_creds.json", "r") as f:
        creds = json.load(f)
    return creds


async def async_main() -> None:
    url: str = (
        "https://music.apple.com/us/playlist/christian-jawns/pl.u-r2yB14xCR4EelLx"
    )
    apple_song_list = await get_apple_music_songs(url=url)
    # apple_song_list: List[Dict[str, str]] = []
    spotify_creds: Dict[str, str] = get_creds()
    create_spotify_playlist(
        song_list=apple_song_list,
        spotify_creds=spotify_creds,
        playlist_name="Christian Jawns",
    )


def main() -> None:
    if __name__ == "__main__":
        asyncio.run(async_main())


main()
