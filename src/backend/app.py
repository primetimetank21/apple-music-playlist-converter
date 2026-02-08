# import os
from typing import Final

import httpx
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from .core import models, settings
from .logger_lib import create_logger

app = FastAPI()

TOKEN_URL: Final[str] = "https://accounts.spotify.com/api/token"


@app.get("/login")
def login():
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
def callback(code: str = Query(None)):
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
