# Apple Music to Spotify Converter - Backend

A FastAPI backend server that orchestrates the conversion of Apple Music playlists to Spotify playlists. Implements Spotify OAuth 2.0 authentication and handles playlist creation with Apple Music song extraction.

## Overview

The backend provides:
- **Spotify OAuth 2.0 Authentication**: Secure login flow for user authorization
- **Apple Music Playlist Parsing**: Extract songs from Apple Music playlist URLs
- **Spotify Playlist Creation**: Create playlists on Spotify with the extracted songs
- **Async Processing**: Background task processing for playlist creation
- **CORS Support**: Cross-origin requests from the frontend at `http://localhost:3000`

## Project Structure

```
backend/
├── app.py                       # FastAPI application and endpoints
├── run_cli.py                   # Command-line interface entry point
├── apple_music_lib/
│   └── get_apple_music.py       # Apple Music playlist extraction logic
├── core/
│   ├── config.py                # Environment variables and settings
│   └── models.py                # Pydantic data models
├── helpers/
│   ├── cli_input.py             # CLI argument parsing
│   └── helper_functions.py      # Playlist creation and utility functions
├── logger_lib/
│   └── create_logger.py         # Logging configuration
├── logs/                        # Application log files
├── .env.example                 # Example environment configuration
└── README.md                    # This file
```

## Setup

### Prerequisites

- Python 3.12 or higher
- uv package manager
- Spotify Developer Account (see [parent README](../../README.md) for Spotify setup)

### Installation

From the project root directory:

```bash
make install
```

This installs all dependencies including FastAPI, Spotipy, Pydantic, and other required packages.

### Environment Configuration

The backend uses environment variables for configuration. Copy the example file:

```bash
cp src/backend/.env.example src/backend/.env
```

Then edit `src/backend/.env` with your Spotify credentials:

```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:3000
LOG_LEVEL=INFO
SCOPE=playlist-modify-public,playlist-modify-private,user-library-read
```

**Key Settings:**
- `CLIENT_ID`: Your Spotify application's client ID
- `CLIENT_SECRET`: Your Spotify application's client secret (keep this secret!)
- `REDIRECT_URI`: Must match your Spotify app settings (default: `http://localhost:3000`)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `SCOPE`: Spotify API scopes (comma-separated)

## Running the Backend

### Standard Approach

From the project root:

```bash
make run-backend
```

The server will start at `http://localhost:8000`

### Direct Command

```bash
uv run uvicorn src.backend.app:app --reload --host 0.0.0.0 --port 8000
```

### Using the CLI

For command-line playlist conversion without the frontend:

```bash
make run-cli ARGS="--apple-playlist-url <URL> --spotify-playlist-name <NAME> [--playlist-description <DESCRIPTION>]"
```

## API Endpoints

### 1. GET `/login`

Returns a redirect to Spotify's authorization page.

**Response:** HTTP 302 redirect to Spotify OAuth URL

**Example:**
```bash
curl http://localhost:8000/login
```

This initiates the OAuth flow:
1. Redirects user to Spotify login
2. User grants permissions
3. Spotify redirects user back to `/callback` with an authorization code

### 2. GET `/callback`

Exchanges the Spotify authorization code for access and refresh tokens.

**Query Parameters:**
- `code` (required): Authorization code from Spotify

**Response:**
```json
{
  "access_token": "spotify_access_token",
  "refresh_token": "spotify_refresh_token",
  "expires_in": 3600
}
```

**Flow:**
1. Receives authorization code from Spotify
2. Exchanges code for access/refresh tokens
3. Returns tokens to frontend
4. Redirects to frontend URL

### 3. POST `/create_playlist`

Creates a Spotify playlist with songs from an Apple Music playlist.

**Request Body:**
```json
{
  "apple_playlist_url": "https://music.apple.com/us/playlist/...",
  "playlist_name": "My Converted Playlist",
  "access_token": "spotify_access_token",
  "public": false,
  "description": "Optional playlist description"
}
```

**Request Fields:**
- `apple_playlist_url` (required): Apple Music playlist URL
- `playlist_name` (required): Name for the new Spotify playlist
- `access_token` (required): Spotify access token from `/callback`
- `public` (optional): Boolean, default false
- `description` (optional): Playlist description

**Response:**
```json
{
  "message": "Playlist creation for 'My Converted Playlist' has been started in the background."
}
```

**Processing:**
- Runs asynchronously in the background
- Extracts songs from Apple Music playlist
- Creates corresponding Spotify playlist
- Returns immediately with status message
- Check logs for actual playlist creation progress/results

**Example:**
```bash
curl -X POST http://localhost:8000/create_playlist \
  -H "Content-Type: application/json" \
  -d '{
    "apple_playlist_url": "https://music.apple.com/us/playlist/...",
    "playlist_name": "My Favorites",
    "access_token": "spotify_token_here"
  }'
```

## Core Modules

### `app.py`

Main FastAPI application with endpoint definitions:
- OAuth login and callback handling
- Playlist creation endpoint
- CORS middleware configuration
- Background task handling

### `core/config.py`

Settings management using Pydantic:
- Loads environment variables from `.env`
- Validates configuration
- Provides typed access to settings

**Settings:**
```python
CLIENT_ID          # Spotify client ID
CLIENT_SECRET      # Spotify client secret
REDIRECT_URI       # OAuth redirect URI
SCOPE              # List of Spotify OAuth scopes
LOG_LEVEL          # Logging level
```

### `core/models.py`

Pydantic data models for request/response validation:
- `TokenResponse`: OAuth token response
- `PlaylistCreateRequest`: Playlist creation request
- `SpotifyAccessToken`: Access token holder
- `SpotifyCredentials`: Spotify credentials
- `CLIArgs`: Command-line arguments

### `apple_music_lib/get_apple_music.py`

Apple Music playlist extraction:
- Parses Apple Music URLs
- Fetches songs from playlist
- Returns song list for Spotify matching

### `helpers/helper_functions.py`

Spotify playlist creation logic:
- Searches for songs on Spotify
- Creates playlists
- Adds songs to created playlists
- Handles API errors and retries

### `helpers/cli_input.py`

Command-line argument handling:
- Parses CLI arguments
- Validates input
- Provides user-friendly error messages

### `logger_lib/create_logger.py`

Logging configuration:
- Structured logging setup
- File and console output
- Configurable log levels
- Formatted log messages

## Configuration

### CORS Settings

Configured to allow requests from:
- `http://localhost:3000` (frontend)
- `http://127.0.0.1:3000` (frontend loopback)
- `http://localhost:8000` (backend)
- `http://127.0.0.1:8000` (backend loopback)

To change CORS origins, edit `app.py`:
```python
allow_origins=[
    "http://localhost:3000",
    # Add more origins here
]
```

### Logging

Logs are written to `src/backend/logs/` directory. Configure the log level in `.env`:

```env
LOG_LEVEL=DEBUG    # Verbose output
LOG_LEVEL=INFO     # Standard level
LOG_LEVEL=WARNING  # Warnings and errors only
```

## Development

### Code Quality

From the project root:

```bash
make lint        # Run linting and auto-fix
make format      # Format code with Ruff
make test        # Run test suite
```

### Running Tests

```bash
make test
```

### Project Documentation

The Spotify API documentation: https://developer.spotify.com/documentation/web-api
Apple Music API documentation (if applicable): https://developer.apple.com/documentation/musickit

## Troubleshooting

### "Invalid client_id" error
- Verify `CLIENT_ID` in `.env` is correct
- Check that the app ID in Spotify Dashboard matches

### "Redirect URI mismatch" error
- Ensure `REDIRECT_URI` in `.env` matches Spotify app settings
- Default should be `http://localhost:3000/`

### "Unauthorized" on playlist creation
- Verify `access_token` is valid and not expired
- Token expires in 1 hour; frontend needs to request new token if needed

### Apple Music songs not found on Spotify
- Some songs may not exist on Spotify
- Check logs for which songs failed to match
- Try with different playlists to verify functionality

### Backend won't start
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Reinstall dependencies
make install

# Try again
make run-backend
```

## Security Considerations

- **Client Secret**: Never commit `.env` file to version control
- **Tokens**: Access tokens expire in 1 hour; use refresh token to get new one
- **CORS**: Restrict `allow_origins` to trusted domains in production
- **Logging**: Do not log sensitive credentials
- **HTTPS**: Use HTTPS in production for OAuth flow

## Architecture

### OAuth 2.0 Flow

```
Frontend                Backend                    Spotify
   |                      |                           |
   |----/login request---->|                           |
   |                       |--auth URL redirect-->|    |
   |<--redirect to auth----|                       |    |
   |                       |                    (user logs in)
   |                       |<-redirect /callback with code-|
   |                       |                       |    |
   |<--redirect w/ tokens--|                       |    |
   |                       |                       |    |
   |-POST /create_playlist-|                       |    |
   |  + access_token       |                       |    |
   |                       |--API requests------->|    |
   |<--confirmation--------|                       |    |
   |                       |--create playlist--->|    |
   |                       |<--confirmation-----|    |
```

### Playlist Creation Flow

```
1. Frontend sends /create_playlist request with:
   - Apple Music URL
   - Spotify access token
   - Playlist metadata

2. Backend extracts songs:
   - Parses Apple Music playlist
   - Returns list of songs

3. Background task processes:
   - Searches each song on Spotify
   - Creates playlist on user's Spotify
   - Adds matched songs to playlist
   - Reports results in logs

4. Frontend polls or checks logs for status
```

## Performance

- **Async Processing**: Playlist creation runs in the background to avoid timeouts
- **Connection Pooling**: HTTPX client reuses connections
- **Retry Logic**: Automatic retries for failed API calls
- **Logging**: Structured logging for debugging and monitoring

## Contributing

To contribute improvements:
1. Follow the code style enforced by Ruff
2. Add tests for new functionality
3. Update this README with new features
4. Ensure all endpoints have proper error handling

## Support

For issues or questions:
- Check the logs in `src/backend/logs/`
- Enable DEBUG logging: `LOG_LEVEL=DEBUG` in `.env`
- Review Spotify API documentation for API-specific errors
- Check the main project README troubleshooting section

## License

See the main project LICENSE file.

---

**Backend Port**: 8000
**Python Version**: 3.12+
**Framework**: FastAPI
**Package Manager**: uv
