import requests
import json
import logging
from logger_lib import create_logger

from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright
from time import sleep
# from pathlib import Path


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


def fetch_songs_via_api_call(
    original_url: str, bearer_auth_token: str
) -> list[dict[str, str]]:
    logger = create_logger(name=__name__, level=logging.INFO)

    logger.info(f"Fetching songs from {original_url}")

    apple_music_songs: list[dict[str, str]] = []

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

    FAIL_LIMIT: int = 5
    WAIT_TIME: int = 5
    failures: int = 0
    offset: int = 0

    playlist_identifier: str = original_url.split("/")[-1]
    BASE_API_URL: str = "https://amp-api.music.apple.com"
    next_url: str = f"/v1/catalog/us/playlists/{playlist_identifier}/tracks"

    while failures < FAIL_LIMIT:
        try:
            params: list[tuple[str, str | int]] = [
                ("l", "en-US"),
                ("offset", offset),
                ("art[url]", "f"),
                ("format[resources]", "map"),
                ("l", "en-US"),
                ("platform", "web"),
            ]

            typed_params: dict[str, str | int] = dict(params)

            url: str = BASE_API_URL + next_url

            response = requests.get(
                url,
                params=typed_params,
                cookies=cookies,
                headers=headers,
            )

            response_json = response.json()

            apple_music_songs += list(response_json["resources"]["songs"].values())
            with open("apple_music_songs.json", "w", encoding="utf-8") as f:
                json.dump(apple_music_songs, f, indent=4)

            logger.info(
                f"Updated apple_music_songs (current length: {len(apple_music_songs)})"
            )

            # Get next url to use for API
            next_url = response_json["next"]

            # Parse the URL
            parsed_url = urlparse(next_url)

            # Get the query parameters
            query_params = parse_qs(parsed_url.query)

            offset = int(query_params["offset"][0])
            logger.debug(f"\toffset: {offset}")

            failures = 0

        except KeyError as key_error:
            if "resources" in str(key_error):
                logger.info(
                    f"Done updating apple_music_songs (final length: {len(apple_music_songs)})"
                )
                break

            failures += 1
            if failures < 2:
                offset += 100
            continue

        except Exception as e:
            logger.error(e)
            failures += 1
            logger.warning(f"Got stuck: {failures}")

        finally:
            sleep(WAIT_TIME)

    return apple_music_songs


async def get_apple_music_songs(url: str) -> list[dict[str, str]]:
    apple_music_songs: list[dict[str, str]] = []

    async with async_playwright() as pr:
        browser = await pr.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        html = await page.content()
        bearer_auth_token = get_bearer_auth_token(html)

        apple_music_songs = fetch_songs_via_api_call(
            original_url=url, bearer_auth_token=bearer_auth_token
        )

    return apple_music_songs
