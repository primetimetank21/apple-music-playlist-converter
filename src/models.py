from pydantic import BaseModel


class SpotifyCredentials(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str


class CLIArgs(BaseModel):
    apple_playlist_url: str
    playlist_description: str
    spotify_playlist_name: str
