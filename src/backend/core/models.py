from typing import Optional

from pydantic import BaseModel


class SpotifyCredentials(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str


class CLIArgs(BaseModel):
    apple_playlist_url: str
    playlist_description: str
    spotify_playlist_name: str


class TokenResponse(BaseModel):
    access_token: str  # used to make API calls (expires in 1hr)
    refresh_token: str  # used to get a new access token later
    expires_in: int


class SpotifyAccessToken(BaseModel):
    access_token: str


class PlaylistCreateRequest(BaseModel):
    apple_playlist_url: str
    playlist_name: str
    access_token: str
    public: Optional[bool] = False
    description: Optional[str] = (
        "Apple Music playlist converted to Spotify playlist! Automated with Python :)"
    )
