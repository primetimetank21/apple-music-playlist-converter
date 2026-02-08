"""Reusable UI components for the Reflex app."""

import reflex as rx

from .state import PlaylistState


def navbar() -> rx.Component:
    """Navigation bar component."""
    return rx.hstack(
        rx.heading("🎵 Apple Music to Spotify Converter", size="7"),
        rx.spacer(),
        rx.cond(
            PlaylistState.is_authenticated,
            rx.badge(
                "Authenticated ✓",
                color_scheme="green",
            ),
            rx.badge(
                "Not Authenticated",
                color_scheme="red",
            ),
        ),
        width="100%",
        padding="1.5em",
        border_bottom="1px solid #e5e7eb",
        background_color=rx.color("gray", 1),
    )


def status_messages() -> rx.Component:
    """Component for displaying status, error, and success messages."""
    return rx.vstack(
        rx.cond(
            PlaylistState.status_message != "",
            rx.callout(
                PlaylistState.status_message,
                icon="info",
                color_scheme="blue",
            ),
        ),
        rx.cond(
            PlaylistState.error_message != "",
            rx.callout(
                PlaylistState.error_message,
                icon="message_circle_warning",
                color_scheme="red",
            ),
        ),
        rx.cond(
            PlaylistState.success_message != "",
            rx.callout(
                PlaylistState.success_message,
                icon="check_check",
                color_scheme="green",
            ),
        ),
        width="100%",
        spacing="2",
    )


def login_section() -> rx.Component:
    """Component for Spotify authentication."""
    return rx.card(
        rx.vstack(
            rx.heading("Step 1: Authenticate with Spotify", size="5"),
            rx.text(
                "Click the button below to log in with your Spotify account.",
                color=rx.color("gray", 7),
            ),
            rx.button(
                "Login with Spotify",
                on_click=[PlaylistState.handle_login],
                size="3",
                color_scheme="green",
                width="100%",
                _hover={"cursor": "pointer"},
            ),
            spacing="1",
            width="100%",
        ),
        width="100%",
    )


def playlist_form() -> rx.Component:
    """Component for entering playlist details."""
    return rx.card(
        rx.vstack(
            rx.heading("Step 2: Enter Playlist Details", size="5"),
            rx.text(
                "Provide the Apple Music playlist URL and details for your new Spotify playlist.",
                color=rx.color("gray", 7),
            ),
            rx.vstack(
                rx.input(
                    placeholder="https://music.apple.com/us/playlist/...",
                    value=PlaylistState.apple_playlist_url,
                    on_change=[PlaylistState.set_apple_playlist_url],
                    type_="url",
                ),
                rx.input(
                    placeholder="My Spotify Playlist",
                    value=PlaylistState.spotify_playlist_name,
                    on_change=[PlaylistState.set_spotify_playlist_name],
                ),
                rx.input(
                    placeholder="Playlist description",
                    value=PlaylistState.playlist_description,
                    on_change=[PlaylistState.set_playlist_description],
                    type_="text",
                ),
                rx.checkbox(
                    "Make playlist public",
                    is_checked=PlaylistState.is_public,
                    on_change=PlaylistState.set_is_public,
                ),
                rx.button(
                    "Create Playlist",
                    on_click=[PlaylistState.create_playlist],
                    size="3",
                    width="100%",
                    is_loading=PlaylistState.is_loading,
                    is_disabled=PlaylistState.is_loading,
                    _hover={"cursor": "pointer"},
                ),
                spacing="1",
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        width="100%",
    )


def footer() -> rx.Component:
    """Footer component."""
    return rx.vstack(
        rx.divider(),
        rx.hstack(
            rx.text(
                "Made with ❤️ for music lovers by TanK",
                color=rx.color("gray", 7),
                font_size="0.9em",
            ),
            rx.spacer(),
            rx.link(
                "GitHub",
                href="https://github.com/primetimetank21/apple-music-playlist-converter",
                is_external=True,
            ),
            width="100%",
        ),
        padding="1.5em",
        width="100%",
    )
