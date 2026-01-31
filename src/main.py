from time import sleep
from typing import Any
import asyncio
import json
import logging

from logger_lib import create_logger
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# from apple_music_lib.get_apple_music import get_apple_music_songs
from apple_music_lib import get_apple_music_songs


# TODO: Add Pydantic for data validation
# TODO: Add way to save songs that failed to be added

type SpotifyUser = dict[str, str | Any] | Any


def create_spotify_playlist(
    song_list: list[dict[str, str]],
    spotify_creds: dict[str, str],
    playlist_name: str,
    scope: str | list[str] = [
        "user-library-modify",
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-library-modify",
        "user-library-read",
        "user-read-private",
    ],
    public: bool = False,
    description: str = "Apple Music playlist converted to Spotify playlist! Automated with Python :)",
) -> None:
    # Create logger
    logger = create_logger(name=__name__, level=logging.INFO)
    # logger = create_logger(name=__name__, level=logging.DEBUG, log_path="./logs")

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
    current_user: SpotifyUser = sp.current_user()

    # Check if playlist already exists
    WAIT_TIME: int = 5
    failed_attempts: int = 0
    FAILED_LIMIT: int = 5
    offset: int = 0
    playlist_id: str = ""

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

            # Get next offset
            # parsed_url = urlparse(user_playlists_response["next"])

            # # Get the query parameters
            # query_params = parse_qs(parsed_url.query)
            # offset = int(query_params["offset"][0])
            if user_playlists_response.get("next", None) is None:
                break
            offset += 50
        except Exception as e:
            logger.exception(e)
            failed_attempts += 1
        finally:
            sleep(WAIT_TIME)

    # Create playlist if it doesn't exist
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


def get_creds() -> dict[str, str]:
    with open("spotify_creds.json", "r") as f:
        creds = json.load(f)
    return creds


def read_json(filename: str) -> list[dict[str, str]]:
    with open(filename, "r") as f:
        apple_song_list = json.load(f)
    return apple_song_list


async def async_main() -> None:
    # TODO: Get input dynamically (i.e., from user)
    #   - playlist url
    #   - playlist name

    url: str = "https://music.apple.com/us/playlist/gymbro/pl.u-55D6X8qU63EXGbj"
    apple_song_list = await get_apple_music_songs(url=url)
    # apple_song_list: list[dict[str, str]] = read_json("apple_music_songs.json")
    spotify_creds: dict[str, str] = get_creds()
    create_spotify_playlist(
        song_list=apple_song_list,
        spotify_creds=spotify_creds,
        playlist_name="GymBro",
    )


def main() -> None:
    if __name__ == "__main__":
        asyncio.run(async_main())
        # print("Hello world!")


main()
