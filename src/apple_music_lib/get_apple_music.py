import json
from typing import Final
from urllib.parse import parse_qs, urlparse

import httpx
from playwright.async_api import Browser, Page, async_playwright
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from logger_lib import create_logger


def get_bearer_auth_token(html: str) -> str:
    if "devToken" not in html:
        raise ValueError("devToken not in html")

    starting_index: int = html.index("devToken")
    end_index: int = html[starting_index : starting_index + 300].index(";")
    bearer_auth_token: str = (
        html[starting_index : starting_index + end_index]
        .replace("&amp", "")
        .replace("devToken=", "")
    )

    return bearer_auth_token


async def fetch_songs_via_api_call(
    original_url: str, bearer_auth_token: str
) -> list[dict[str, str]]:
    logger = create_logger(name=fetch_songs_via_api_call.__name__)
    logger.debug("Fetching songs via API call")
    logger.info(f"Fetching songs from {original_url}")

    apple_music_songs: list[dict[str, str]] = []
    playlist_identifier: str = original_url.split("/")[-1]
    BASE_API_URL: Final[str] = "https://amp-api.music.apple.com"

    cookies = {"geo": "US"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://music.apple.com/",
        "Authorization": f"Bearer {bearer_auth_token}",
        "Origin": "https://music.apple.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4",
    }

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=5, max=60),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
        reraise=True,
    )
    async def fetch_page(*, client: httpx.AsyncClient, url: str, offset: int):
        """Fetch a single page of songs with automatic retry logic."""
        params = {
            "l": "en-US",
            "offset": offset,
            "art[url]": "f",
            "format[resources]": "map",
            "platform": "web",
        }
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(
        cookies=cookies,
        headers=headers,
        timeout=30.0,
    ) as client:
        next_url: str = f"/v1/catalog/us/playlists/{playlist_identifier}/tracks"
        offset: int = 0

        while True:
            try:
                url = BASE_API_URL + next_url
                response_json = await fetch_page(client=client, url=url, offset=offset)
                logger.debug(f"{response_json.keys()=}")

                apple_music_songs += list(response_json["resources"]["songs"].values())
                with open("apple_music_songs.json", "w", encoding="utf-8") as f:
                    json.dump(apple_music_songs, f, indent=4)

                logger.info(
                    f"Updated apple_music_songs (current length: {len(apple_music_songs)})"
                )

                # Parse next URL for pagination
                next_url = response_json.get("next", None)
                if not next_url:
                    logger.info(
                        f"Done updating apple_music_songs (final length: {len(apple_music_songs)})"
                    )
                    break

                parsed_url = urlparse(next_url)
                query_params = parse_qs(parsed_url.query)
                offset = int(query_params["offset"][0])
                logger.debug(f"Next offset: {offset}")

            except KeyError as e:
                if "resources" in str(e):
                    logger.info(
                        f"Done updating apple_music_songs (final length: {len(apple_music_songs)})"
                    )
                    break
                raise
            except Exception as e:
                logger.exception(f"Error fetching songs: {e}")
                raise

    return apple_music_songs


async def get_apple_music_songs(url: str) -> list[dict[str, str]]:
    apple_music_songs: list[dict[str, str]] = []

    async with async_playwright() as pr:
        browser: Browser = await pr.firefox.launch(headless=True)
        page: Page = await browser.new_page()
        await page.goto(url)

        html: str = await page.content()
        bearer_auth_token: str = get_bearer_auth_token(html)

        apple_music_songs = await fetch_songs_via_api_call(
            original_url=url, bearer_auth_token=bearer_auth_token
        )

    return apple_music_songs
