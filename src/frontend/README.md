# Apple Music to Spotify Converter - Frontend

A modern web frontend for converting Apple Music playlists to Spotify playlists. Built with [Reflex](https://reflex.dev), a full-stack Python framework that compiles to React.

## Overview

This frontend provides a user-friendly interface for:
- Authenticating with Spotify via OAuth 2.0
- Converting Apple Music playlist URLs to Spotify playlists
- Customizing playlist metadata (name, description, public/private status)
- Real-time status updates during the conversion process

## Prerequisites

- **Python**: 3.12 or higher
- **uv**: The project's package manager (will be installed automatically if needed)
- **Backend Server**: Apple Music to Spotify converter backend running at `http://localhost:8000`
- **Spotify Developer Account**: For OAuth credentials (Client ID and Secret)

## Installation

### 1. Install Dependencies

From the root directory:

```bash
make install
```

This installs all Python dependencies using `uv` (the project's package manager).

### 2. Set Up Environment Variables

Create a `.env` file in the backend directory with your Spotify credentials:

```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:3000/
```

See [OAUTH_SETUP.md](../../OAUTH_SETUP.md) for detailed Spotify OAuth setup instructions.

## Running the Application

### Start the Backend

From the root directory:

```bash
make run-backend
```

The backend will start at `http://localhost:8000`

### Start the Frontend

From the root directory:

```bash
make run-frontend
```

The frontend will start at `http://localhost:3000`

You should see output similar to:
```
───────────────────────────────── Starting Reflex App ──────────────────────────────
[HH:MM:SS] Compiling: ━━━━━━━━━━━━━━━━━━━━━ 100% 16/16 0:00:00
───────────────────────────────── App Running ──────────────────────────────────
App running at: http://localhost:3000
```

## Usage

### Step 1: Authenticate with Spotify
1. Click the "Login with Spotify" button
2. You'll be redirected to Spotify's login page
3. Grant the required permissions
4. You'll be redirected back to the app with your access token

### Step 2: Convert Playlist
1. Paste your Apple Music playlist URL in the "Apple Music Playlist URL" field
2. Enter your desired Spotify playlist name
3. (Optional) Add a playlist description
4. Toggle whether the playlist should be public or private
5. Click "Create Playlist"
6. Monitor the status messages for progress

## Project Structure

```
frontend/
├── frontend/
│   ├── __init__.py              # Package initialization
│   ├── frontend.py              # Main Reflex app entry point
│   ├── state.py                 # State management for authentication and form data
│   ├── components.py            # Reusable UI components
│   └── config.py                # Configuration settings
├── assets/                      # Static assets (images, icons, etc.)
├── rxconfig.py                  # Reflex configuration
├── reflex.json                  # Reflex project metadata
└── README.md                    # This file
```

## Architecture

### OAuth 2.0 Flow

The frontend implements Spotify's OAuth 2.0 Authorization Code Grant flow:

```
1. User clicks "Login with Spotify"
         ↓
2. Frontend redirects to backend /login endpoint
         ↓
3. Backend returns Spotify's authorization URL
         ↓
4. Spotify redirects user to their login page
         ↓
5. User grants permissions
         ↓
6. Spotify redirects back to app with ?code=...
         ↓
7. JavaScript intercepts the code
         ↓
8. JavaScript calls backend /callback endpoint
         ↓
9. Backend exchanges code for access tokens
         ↓
10. Tokens stored in browser localStorage and cookies
         ↓
11. Frontend marks user as authenticated
         ↓
12. UI shows playlist conversion form
```

### State Management

The `PlaylistState` class in `state.py` manages:
- **Authentication State**: `access_token`, `refresh_token`, `is_authenticated`
- **Form Data**: `apple_playlist_url`, `spotify_playlist_name`, `playlist_description`, `is_public`
- **UI State**: `is_loading`, `status_message`, `error_message`, `success_message`

### Components

- **navbar()**: Header with app title and authentication status badge
- **login_section()**: Button to initiate Spotify login
- **status_messages()**: Displays status, error, and success messages
- **playlist_form()**: Form for entering playlist details and creating playlists
- **footer()**: Footer with project links

## API Endpoints

The frontend communicates with these backend endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/login` | GET | Get Spotify authorization URL |
| `/callback` | GET/POST | Exchange auth code for tokens |
| `/create_playlist` | POST | Create a new Spotify playlist with songs |
| `/verify_token` | POST | Verify if a token is still valid |

## Configuration

### Backend URL

To change the backend URL from the default `http://localhost:8000`, edit:
- Backend URL in `state.py`
- CORS settings in the backend `app.py` to include your frontend URL

### Spotify OAuth

Update these in the backend `.env` file:
- `CLIENT_ID`: Your Spotify application's client ID
- `CLIENT_SECRET`: Your Spotify application's client secret
- `REDIRECT_URI`: Must match your Spotify app settings (default: `http://localhost:3000/`)

## Features

- 🔐 **Spotify OAuth 2.0**: Secure authentication without storing passwords
- 🎵 **Apple Music Support**: Parse and extract songs from Apple Music playlists
- 📝 **Customizable Metadata**: Edit playlist name, description, and visibility
- 📊 **Real-time Status**: See conversion progress with detailed messages
- 🌐 **Modern UI**: Clean, responsive interface built with Reflex
- ♻️ **Background Processing**: Conversions happen in the background
- 🔄 **Token Management**: Automatic token storage and refresh handling

## Troubleshooting

### Frontend won't start
```bash
# Clear Reflex build cache
rm -rf .web

# Reinstall dependencies
make install

# Try again
make run-frontend
```

### OAuth redirect not working
1. Verify backend is running: `make run-backend`
2. Check CORS settings in backend `app.py`
3. Ensure Spotify app's Redirect URI matches `http://localhost:3000/`
4. Check browser console for JavaScript errors (F12)

### Tokens not being saved
1. Check browser's localStorage: Open DevTools → Application → Local Storage
2. Verify cookies are being set: DevTools → Application → Cookies
3. Check backend logs for `/callback` request

### Playlist creation fails
1. Verify Spotify token is still valid
2. Check that your Apple Music URL is correctly formatted
3. See backend logs for detailed error messages

## Development

### Enable Debug Mode

In `state.py`:
```python
PlaylistState.debug = True  # Add debugging output
```

### View Network Requests

Open browser DevTools (F12) and check the Network tab to see:
- `/login` requests to backend
- `/callback` requests for token exchange
- `/create_playlist` requests for playlist creation

### Hot Reload

Reflex automatically reloads the frontend when you save files. No need to manually restart!

## Common Issues

**Q: "Argument missing for parameter 'self'" error**
- A: This happens when event handlers are incorrectly bound. Make sure event handlers don't take additional parameters beyond those provided by the event.

**Q: Tokens disappear after page refresh**
- A: Tokens are stored in localStorage. Check DevTools to ensure they're being saved correctly.

**Q: "Cannot access attribute 'query_params'" error**
- A: This is a Reflex version compatibility issue. The frontend handles OAuth entirely in JavaScript, so this shouldn't be a problem with the current implementation.

## Performance Tips

- If you experience issues, clear the `.web` build directory: `rm -rf .web`
- Use the browser cache for faster page loads
- LocalStorage is used for tokens to avoid repeated authentication requests
- Dependencies are managed centrally via `make install` for efficiency

## Security

- 🔒 Tokens are stored in browser storage (same origin only)
- 🔐 Tokens are NOT sent to backend on every request (only when explicitly needed)
- ✅ CORS is configured to only accept requests from `http://localhost:3000`
- 🛡️ OAuth flow uses secure HTTPS to Spotify (in production)

## Contributing

Found a bug or have a feature request? Please open an issue or submit a pull request!

## Support

For issues with:
- **Reflex Framework**: See [Reflex docs](https://reflex.dev/docs)
- **Spotify API**: See [Spotify API docs](https://developer.spotify.com/documentation/web-api)
- **This Project**: Check the main project README or open an issue

## License

See the main project LICENSE file.

## Changelog

### v0.1.0 (Current)
- Initial frontend release
- Spotify OAuth 2.0 implementation
- Basic playlist conversion UI
- Status message display
- Form validation

---

**Last Updated**: February 2026
**Python Version**: 3.12+
**Node Version**: 16+
