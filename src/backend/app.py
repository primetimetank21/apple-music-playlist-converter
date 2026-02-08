# import os
from typing import Any, Final

import httpx
from fastapi import BackgroundTasks, FastAPI, Query
from fastapi.responses import RedirectResponse

from .apple_music_lib import get_apple_music_songs
from .core import models, settings
from .helpers import create_spotify_playlist
from .logger_lib import create_logger

app = FastAPI()

TOKEN_URL: Final[str] = "https://accounts.spotify.com/api/token"


@app.get("/login")
async def login():
    """Redirect user to Spotify's login page."""
    logger = create_logger(name=login.__name__)
    auth_url: str = (
        "https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={settings.CLIENT_ID}&"
        f"scope={' '.join(settings.SCOPE)}&redirect_uri={settings.REDIRECT_URI}"
    )
    logger.debug(f"Redirecting user to {auth_url}")
    return RedirectResponse(auth_url)


# TODO: Create frontend to receive the access token and refresh token
@app.get("/callback", response_model=models.TokenResponse)
async def callback(code: str = Query(None)):
    """Swap the code for an Access Token and Refresh Token."""
    logger = create_logger(name=callback.__name__)
    logger.debug(f"Received code: {code}")

    if not code:
        return {"error": "Authorization failed"}

    # Payload to exchange code for tokens
    payload: dict[str, str] = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.REDIRECT_URI,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
    }

    response = httpx.post(TOKEN_URL, data=payload)
    token_response = response.json()

    token_data = models.TokenResponse(**token_response)

    return token_data


# TODO: Create frontend to call this endpoint with the access token and playlist data
@app.post("/create_playlist")
async def create_spotify_playlist_endpoint(
    background_tasks: BackgroundTasks, playlist_data: models.PlaylistCreateRequest
):
    logger = create_logger(name=create_spotify_playlist_endpoint.__name__)
    logger.debug(f"Received request to create playlist: {playlist_data.playlist_name}")

    # Get Apple Music songs from playlist url
    logger.debug(
        f"Fetching songs from Apple Music playlist: {playlist_data.apple_playlist_url}"
    )
    song_list: list[dict[str, str]] = await get_apple_music_songs(
        url=playlist_data.apple_playlist_url
    )
    logger.debug(f"Fetched {len(song_list)} songs from Apple Music playlist")

    # Get rest of args needed for create_spotify_playlist function
    args: dict[str, Any] = {
        "song_list": song_list,
        "spotify_creds": models.SpotifyAccessToken(
            access_token=playlist_data.access_token
        ),
        "playlist_name": playlist_data.playlist_name,
        "scope": settings.SCOPE,
        "public": playlist_data.public,
        "description": playlist_data.description,
    }
    logger.debug(f"Calling create_spotify_playlist with args: {args}")

    # Add create_spotify_playlist to background tasks
    background_tasks.add_task(create_spotify_playlist, **args)

    return {
        "message": f"Playlist creation for '{playlist_data.playlist_name}' has been started in the background."
    }
