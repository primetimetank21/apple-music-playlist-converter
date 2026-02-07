[![Python Versions](https://github.com/primetimetank21/apple-music-playlist-converter/actions/workflows/python-versions.yml/badge.svg)](https://github.com/primetimetank21/apple-music-playlist-converter/actions/workflows/python-versions.yml)

# Apple Music Playlist Converter

## Purpose

This tool automates the process of converting Apple Music playlists to Spotify playlists. It retrieves songs from an Apple Music playlist URL and creates a corresponding Spotify playlist with the same tracks, allowing you to easily migrate your music collections between platforms.

## Project Structure

```
apple-music-playlist-converter/
├── src/
│   ├── main.py                  # Entry point of the application
│   ├── config.py                # Configuration management (environment variables)
│   ├── models.py                # Data models and type definitions
│   ├── apple_music_lib/         # Apple Music integration module
│   │   └── get_apple_music.py   # Fetches songs from Apple Music playlists
│   ├── helpers/                 # Utility functions
│   │   ├── cli_input.py         # Command-line argument parser
│   │   └── helper_functions.py  # Shared utility functions
│   └── logger_lib/              # Logging configuration
│       └── create_logger.py     # Logger setup
├── logs/                        # Application log files
├── Makefile                     # Build and development tasks
├── pyproject.toml               # Project metadata and dependencies
├── README.md                    # This file
└── apple_music_songs.json       # Sample/cached Apple Music data
```

## Setup

### Prerequisites

- Python 3.12 or higher
- Spotify Developer Account (for API credentials)
- uv package manager
- Running on Linux/MacOS (Windows not supported yet unless WSL)

### Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:primetimetank21/apple-music-playlist-converter.git
   cd apple-music-playlist-converter
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```
   This command installs all required packages and sets up pre-commit hooks using `uv`.

3. **Configure Environment Variables:**
   
   Create a `.env` file in the project root with your Spotify API credentials:
   ```env
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   REDIRECT_URI=http://localhost:8888/callback
   LOG_LEVEL=INFO
   SCOPE=playlist-modify-public,playlist-modify-private
   ```
   
   To get your Spotify credentials:
   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Copy your `Client ID` and `Client Secret`
   - Set your Redirect URI to match the one in your `.env` file

## Running the Application

Use the following command to convert an Apple Music playlist:

```bash
make run ARGS="--apple-playlist-url <URL> --spotify-playlist-name <NAME> [--playlist-description <DESCRIPTION>]"
```

### Arguments

- `--apple-playlist-url` (required): The URL of the Apple Music playlist to convert
- `--spotify-playlist-name` (required): The name for the new Spotify playlist
- `--playlist-description` (optional): Description for the Spotify playlist (defaults to "Apple Music playlist converted to Spotify playlist! Automated with Python :)")

### Example

```bash
make run ARGS="--apple-playlist-url 'https://music.apple.com/us/playlist/...' --spotify-playlist-name 'My Favorite Songs' --playlist-description 'My favorite tracks from Apple Music'"
```

## Development

Additional make commands for development:

- `make lint` - Run code linting and auto-fix issues
- `make format` - Format code with Ruff
- `make test` - Run test suite
- `make clean` - Remove build artifacts and cache files

## Dependencies

Key dependencies include:
- **spotipy** - Spotify Web API client
- **pydantic** - Data validation and settings management
- **pytest** - Testing framework
- **ruff** - Python linter and formatter
- **tenacity** - Retry logic utilities