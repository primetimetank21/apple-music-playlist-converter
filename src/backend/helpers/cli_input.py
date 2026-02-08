import argparse


def create_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Apple Music playlists to Spotify playlists."
    )
    parser.add_argument(
        "--apple-playlist-url",
        type=str,
        required=True,
        help="The URL of the Apple Music playlist to convert.",
    )
    parser.add_argument(
        "--spotify-playlist-name",
        type=str,
        required=True,
        help="The name of the Spotify playlist to create.",
    )
    parser.add_argument(
        "--playlist-description",
        type=str,
        required=False,
        default="Apple Music playlist converted to Spotify playlist! Automated with Python :)",
        help="The description of the Spotify playlist to create.",
    )
    return parser
