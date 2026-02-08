"""Main Reflex app for Apple Music to Spotify Playlist Converter."""

import reflex as rx

from .components import (
    footer,
    login_section,
    navbar,
    playlist_form,
    status_messages,
)
from .state import PlaylistState


def index() -> rx.Component:
    """Main page of the application."""
    return rx.container(
        rx.vstack(
            navbar(),
            rx.box(
                rx.vstack(
                    status_messages(),
                    rx.cond(
                        PlaylistState.is_authenticated,
                        playlist_form(),
                        login_section(),
                    ),
                    spacing="0",
                    padding="2em",
                ),
                width="100%",
            ),
            footer(),
            spacing="0",
            min_height="100vh",
        ),
        max_width="100%",
        padding="0",
    )


# Create the Reflex app
app = rx.App()
app.add_page(index, route="/", on_load=PlaylistState.on_load_handler)
