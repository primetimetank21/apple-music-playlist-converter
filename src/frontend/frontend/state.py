"""State management for the Reflex frontend."""

import httpx
import reflex as rx

BACKEND_URL: str = "http://localhost:8000"


class PlaylistState(rx.State):
    """State for tracking playlist conversion progress."""

    # Authentication state
    access_token: str = ""
    # refresh_token: str = ""
    is_authenticated: bool = False

    # Form state
    apple_playlist_url: str = ""
    spotify_playlist_name: str = ""
    playlist_description: str = (
        "Apple Music playlist converted to Spotify playlist! Automated with Python :)"
    )
    is_public: bool = False

    # Status state
    is_loading: bool = False
    status_message: str = ""
    error_message: str = ""
    success_message: str = ""

    def __init__(self, *args, **kwargs):
        """Initialize and check for stored auth state."""
        super().__init__(*args, **kwargs)
        # This won't work server-side, but at least attempt it
        self._restore_auth_state()

    @rx.event
    def on_load_handler(self):
        """Handler to run when the app loads."""
        token = self.router.url.query_parameters.get("access_token", "")
        if token:
            self.access_token = token
            self.is_authenticated = True
            self.is_loading = False
            self.reset_messages()
            self.success_message = "Successfully authenticated with Spotify!"

            # Clear the access token from the URL by redirecting to home
            yield rx.redirect("/")

    def _restore_auth_state(self):
        """Try to restore authentication state from browser storage or URL params."""
        try:
            # Check if auth_ready flag is in URL
            if hasattr(self.router, "query_params"):
                params = getattr(self.router, "query_params", {})
                if params.get("auth_ready"):
                    print(
                        "auth_ready flag detected in URL, trying to restore tokens..."
                    )
                    # Tokens should be in browser storage
                    # This method will be called by JavaScript when it detects them
        except Exception as e:
            print(f"Could not restore auth state: {e}")

    def reset_messages(self):
        """Reset all status messages."""
        self.status_message = ""
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def set_apple_playlist_url(self, value: str):
        """Set Apple Music playlist URL."""
        self.apple_playlist_url = value

    @rx.event
    def set_spotify_playlist_name(self, value: str):
        """Set Spotify playlist name."""
        self.spotify_playlist_name = value

    @rx.event
    def set_playlist_description(self, value: str):
        """Set playlist description."""
        self.playlist_description = value

    @rx.event
    def set_is_public(self, value: bool):
        """Set playlist public/private."""
        self.is_public = value

    @rx.event
    def handle_login(self):
        """Get Spotify authorization URL and redirect browser."""
        self.reset_messages()
        self.is_loading = True
        self.status_message = "Redirecting to Spotify..."

        # TODO: make backend URL configurable
        return rx.redirect(f"{BACKEND_URL}/login")

    @rx.event
    async def create_playlist(self):
        """Send the playlist creation request to the backend."""
        self.reset_messages()

        # Validate form inputs
        if not self.apple_playlist_url:
            self.error_message = "Please enter an Apple Music playlist URL"
            return

        if not self.spotify_playlist_name:
            self.error_message = "Please enter a Spotify playlist name"
            return

        if not self.access_token:
            self.error_message = "Please authenticate with Spotify first"
            return

        self.is_loading = True
        self.status_message = "Creating playlist..."

        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "apple_playlist_url": self.apple_playlist_url,
                    "playlist_name": self.spotify_playlist_name,
                    "access_token": self.access_token,
                    "public": self.is_public,
                    "description": self.playlist_description,
                }

                response = await client.post(
                    f"{BACKEND_URL}/create_playlist", json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    self.success_message = data.get(
                        "message", "Playlist created successfully!"
                    )
                    # Reset form
                    self.apple_playlist_url = ""
                    self.spotify_playlist_name = ""
                    self.status_message = ""
                else:
                    self.error_message = (
                        f"Failed to create playlist: {response.status_code}"
                    )
        except Exception as e:
            self.error_message = f"Error creating playlist: {str(e)}"
        finally:
            self.is_loading = False
