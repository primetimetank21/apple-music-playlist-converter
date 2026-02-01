from pydantic import BaseModel


class SpotifyCredentials(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str
