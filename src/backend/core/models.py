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
    access_token: str  # ACCESS_TOKEN: Used to make API calls (expires in 1hr)
    refresh_token: str  # REFRESH_TOKEN: Used to get a new access token later
    expires_in: int
