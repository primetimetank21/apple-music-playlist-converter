from time import sleep
from typing import Any, Final, Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ..core import models, settings
from ..logger_lib import create_logger

type SpotifyUser = dict[str, str | Any] | Any
WAIT_TIME: Final[int] = 5


def get_playlist_id(
    *,
    sp: spotipy.Spotify,
    current_user: SpotifyUser,
    playlist_name: str,
    public: bool,
    description: str,
) -> str:
    """Get Spotify playlist ID. If playlist doesn't exist, create it."""
    logger = create_logger(name=get_playlist_id.__name__)
    logger.debug("Getting playlist ID")

    failed_attempts: int = 0
    FAILED_LIMIT: Final[int] = 5
    offset: int = 0

    playlist_id: str = ""

    # Placeholder function to get playlist ID
    while all([playlist_id == "", failed_attempts < FAILED_LIMIT]):
        try:
            user_playlists_response: Any = sp.user_playlists(
                user=current_user["id"], limit=50, offset=offset
            )
            logger.debug(f"{user_playlists_response=}\n{failed_attempts=}\n")

            # Get playlist ID if it exists
            for playlist in user_playlists_response["items"]:
                if playlist_name == playlist["name"]:
                    playlist_id = playlist["id"]
                    logger.info(f"Found playlist: '{playlist_name}'")
                    break

            # Create playlist if it doesn't exist
            if playlist_id:
                break

            if user_playlists_response.get("next", None) is None:
                break
            offset += 50
        except Exception as e:
            logger.exception(e)
            failed_attempts += 1
        finally:
            sleep(WAIT_TIME)

    if not playlist_id:
        logger.info(f"Playlist '{playlist_name}' not found. Creating...")
        create_user_playlist_response: Any = sp.user_playlist_create(
            user=current_user["id"],
            name=playlist_name,
            public=public,
            description=description,
        )
        logger.debug(f"{create_user_playlist_response=}\n")
        playlist_id = create_user_playlist_response["id"]
        logger.info(f"Created playlist: '{playlist_name}'")

    return playlist_id


def add_songs_to_playlist(
    sp: spotipy.Spotify,
    playlist_id: str,
    song_list: list[dict[str, str]],
    playlist_name: str,
) -> None:
    # Create logger
    logger = create_logger(name=add_songs_to_playlist.__name__)
    logger.debug("Adding songs to playlist")

    # Add songs to playlist
    for song_data in song_list:
        try:
            # Search Spotify for song
            song_name, song_artist = (
                song_data["attributes"]["name"],  # type: ignore
                song_data["attributes"]["artistName"],  # type: ignore
            )

            song_search_response: Any = sp.search(
                q=f"track:'{song_name}' artist:'{song_artist}'", type="track", limit=1
            )
            new_song_uri = song_search_response["tracks"]["items"][0]["id"]
            sleep(1.5)

            # Add song to playlist
            add_song_to_playlist_response = sp.playlist_add_items(
                playlist_id=playlist_id, items=[new_song_uri]
            )
            logger.info(f"Added '{song_name}' by '{song_artist}' to '{playlist_name}'")
            logger.debug(f"{add_song_to_playlist_response=}\n")
        except IndexError:
            try:
                logger.error(
                    f"Failed to add '{song_name}' by '{song_artist}' to '{playlist_name}'"
                )
            except Exception:
                logger.error(f"Failed to add a song to '{playlist_name}'")
        except Exception as e:
            logger.exception(e)
        finally:
            sleep(WAIT_TIME)

        # Search for song
        # sp.search(
        #     q=song_list[0]["artist"] + " " + song_list[0]["name"],
        #     type="track",
        #     limit=1,
        # )

        # q="remaster%2520track%3ADoxy%2520artist%3AMiles%2520Davis"
        # q="track:Doxy artist:Miles Davis"
        # q="track:'So Good' artist:'Torey D Shaun'"
        # song["attributes"]["name"], song["attributes"]["artistName"]
        # song_search_response = sp.search(q="track: Bounce! artist:Vennisay", type="track")
        # song_search_response = sp.search(q=q, type="track", limit=1)
        # logger.info(f"\n{song_search_response=}\n")
        # with open("song_search_response1.json", "w") as f:
        #     json.dump(song_search_response, f, indent=4)


def get_auth_and_current_user(
    *,
    spotify_creds: models.SpotifyCredentials | models.SpotifyAccessToken,
    scope: str | list[str],
) -> tuple[spotipy.Spotify, SpotifyUser]:
    """Create a Spotify API Client and get the current user info."""
    logger = create_logger(name=get_auth_and_current_user.__name__)
    logger.debug("Authenticating Spotify user")

    # Authenticate user
    if isinstance(spotify_creds, models.SpotifyCredentials):
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=spotify_creds.client_id,
                client_secret=spotify_creds.client_secret,
                redirect_uri=spotify_creds.redirect_uri,
                scope=scope,
            )
        )
    elif isinstance(spotify_creds, models.SpotifyAccessToken):
        sp = spotipy.Spotify(auth=spotify_creds.access_token)
    else:
        raise ValueError("Invalid spotify credentials")

    # Get current user info
    logger.debug("Getting current Spotify user")
    current_user: SpotifyUser = sp.current_user()
    logger.debug(f"{current_user=}\n")

    return (sp, current_user)


def create_spotify_playlist(
    *,
    song_list: list[dict[str, str]],
    spotify_creds: models.SpotifyCredentials | models.SpotifyAccessToken,
    playlist_name: str,
    scope: Optional[str | list[str]] = None,
    public: bool = False,
    description: str,
) -> None:
    # Create logger
    logger = create_logger(name=create_spotify_playlist.__name__)
    logger.debug("Creating Spotify playlist")
    if not scope:
        scope = settings.SCOPE
        logger.debug(f"Using default scope: {scope=}")

    # Get auth and current user
    sp, current_user = get_auth_and_current_user(
        spotify_creds=spotify_creds, scope=scope
    )

    # Check if playlist already exists. If not, create it.
    playlist_id: str = get_playlist_id(
        sp=sp,
        current_user=current_user,
        playlist_name=playlist_name,
        public=public,
        description=description,
    )

    # Add songs to playlist
    add_songs_to_playlist(
        sp=sp, playlist_id=playlist_id, song_list=song_list, playlist_name=playlist_name
    )
