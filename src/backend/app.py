# import os
from typing import Final

import httpx
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from ..config import settings
from ..models import TokenResponse

app = FastAPI()

TOKEN_URL: Final[str] = "https://accounts.spotify.com/api/token"


@app.get("/login")
def login():
    """Redirect user to Spotify's login page."""
    auth_url: str = (
        "https://accounts.spotify.com/authorize?"
        f"response_type=code&client_id={settings.CLIENT_ID}&"
        f"scope={' '.join(settings.SCOPE)}&redirect_uri={settings.REDIRECT_URI}"
    )
    return RedirectResponse(auth_url)


# TODO: Create frontend to receive the access token and refresh token
@app.get("/callback", response_model=TokenResponse)
def callback(code: str = Query(None)):
    """Swap the code for an Access Token and Refresh Token."""
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

    token_data = TokenResponse(**token_response)

    # ACCESS_TOKEN: Used to make API calls (expires in 1hr)
    # REFRESH_TOKEN: Used to get a new access token later
    return token_data
