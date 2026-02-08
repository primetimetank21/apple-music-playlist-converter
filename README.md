[![Python Versions](https://github.com/primetimetank21/apple-music-playlist-converter/actions/workflows/python-versions.yml/badge.svg)](https://github.com/primetimetank21/apple-music-playlist-converter/actions/workflows/python-versions.yml)

# Apple Music Playlist Converter

## Purpose

This tool automates the process of converting Apple Music playlists to Spotify playlists. It retrieves songs from an Apple Music playlist URL and creates a corresponding Spotify playlist with the same tracks, allowing you to easily migrate your music collections between platforms.

## Project Structure

```
apple-music-playlist-converter/
├── src/
│   ├── backend/                      # FastAPI backend server
│   │   ├── app.py                    # FastAPI application and endpoints
│   │   ├── run_cli.py                # CLI entry point
│   │   ├── apple_music_lib/          # Apple Music integration module
│   │   │   └── get_apple_music.py    # Fetches songs from Apple Music playlists
│   │   ├── core/                     # Core business logic
│   │   │   ├── config.py             # Configuration management
│   │   │   └── models.py             # Data models and type definitions
│   │   ├── helpers/                  # Utility functions
│   │   │   ├── cli_input.py          # Command-line argument parser
│   │   │   └── helper_functions.py   # Shared utility functions
│   │   └── logger_lib/               # Logging configuration
│   │       └── create_logger.py      # Logger setup
│   │
│   └── frontend/                     # Reflex web frontend
│       ├── frontend/
│       │   ├── frontend.py           # Main Reflex app
│       │   ├── state.py              # State management
│       │   ├── components.py         # UI components
│       ├── rxconfig.py               # Reflex configuration
│       ├── assets/                   # Static assets
│       └── README.md                 # Frontend documentation
│
├── Makefile                         # Build and development tasks
├── pyproject.toml                   # Project metadata and dependencies
├── README.md                        # This file
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
   REDIRECT_URI=http://localhost:8000/callback
   LOG_LEVEL=INFO
   SCOPE=playlist-modify-public,playlist-modify-private,user-library-read
   ```
   
   To get your Spotify credentials:
   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Copy your `Client ID` and `Client Secret`
   - Set your Redirect URI to `http://localhost:8000/callback`

## Running the Application

The application consists of two parts: a backend server (FastAPI) and a frontend web interface (Reflex).

### Option 1: Web Interface (Recommended)

**Start the backend:**
```bash
make run-backend
```
The backend will run at `http://localhost:8000`

**In another terminal, start the frontend:**
```bash
make run-frontend
```
The frontend will run at `http://localhost:3000`

Then open your browser to `http://localhost:3000` and use the web interface to:
1. Login with Spotify via OAuth 2.0
2. Enter your Apple Music playlist URL
3. Customize the Spotify playlist name and description
4. Create the playlist

### Option 2: Command Line Interface

Use the CLI to convert a playlist:

```bash
make run-cli ARGS="--apple-playlist-url <URL> --spotify-playlist-name <NAME> [--playlist-description <DESCRIPTION>]"
```

#### Arguments

- `--apple-playlist-url` (required): The URL of the Apple Music playlist to convert
- `--spotify-playlist-name` (required): The name for the new Spotify playlist
- `--playlist-description` (optional): Description for the Spotify playlist

#### Example

```bash
make run-cli ARGS="--apple-playlist-url 'https://music.apple.com/us/playlist/...' --spotify-playlist-name 'My Favorite Songs'"
```

## Development

Additional make commands for development:

- `make lint` - Run code linting and auto-fix issues
- `make format` - Format code with Ruff
- `make test` - Run test suite
- `make clean` - Remove build artifacts and cache files
- `make all` - Run install, lint, format, and test

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Spotipy** - Spotify Web API client
- **Pydantic** - Data validation and settings management

### Frontend
- **Reflex** - Full-stack Python framework (compiles to React)
- **Spotify OAuth 2.0** - Secure authentication

### Tools
- **uv** - Fast Python package manager
- **Ruff** - Python linter and formatter
- **Pytest** - Testing framework

## Dependencies

Key dependencies include:
- **spotipy** - Spotify Web API client
- **pydantic** - Data validation and settings management
- **pytest** - Testing framework
- **ruff** - Python linter and formatter
- **tenacity** - Retry logic utilities