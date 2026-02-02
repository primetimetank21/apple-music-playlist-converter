import logging
from pathlib import Path
from typing import Final, Optional

from config import settings

LEVEL_COLOURS: Final[list[tuple[int, str]]] = [
    (logging.DEBUG, "\x1b[40;1m"),
    (logging.INFO, "\x1b[34;1m"),
    (logging.WARNING, "\x1b[33;1m"),
    (logging.ERROR, "\x1b[31m"),
    (logging.CRITICAL, "\x1b[41m"),
]


class _ColourFormatter(logging.Formatter):
    # ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher
    # It starts off with a format like \x1b[XXXm where XXX is a semicolon separated list of commands
    # The important ones here relate to colour.
    # 30-37 are black, red, green, yellow, blue, magenta, cyan and white in that order
    # 40-47 are the same except for the background
    # 90-97 are the same but "bright" foreground
    # 100-107 are the same as the bright ones but for the background.
    # 1 means bold, 2 means dim, 0 means reset, and 4 means underline.

    def __init__(self, logger_name: str) -> None:
        super().__init__()
        self.logger_name = logger_name
        self.FORMATS: Final[dict[int, logging.Formatter]] = {
            level: logging.Formatter(
                # f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
                f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m{logger_name}\x1b[0m %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            for level, colour in LEVEL_COLOURS
        }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


def create_logger(
    *,
    name: str,
    handler: Optional[logging.Handler] = None,
    formatter: Optional[logging.Formatter] = None,
    level: Optional[int] = None,
) -> logging.Logger:
    if not level:
        level = settings.LOG_LEVEL

    if not handler:
        handler = logging.StreamHandler()

    if not formatter:
        if isinstance(handler, logging.StreamHandler):
            formatter = _ColourFormatter(logger_name=name)
        else:
            dt_fmt = "%Y-%m-%d %H:%M:%S"
            formatter = logging.Formatter(
                "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
            )

    logger = logging.getLogger(name)

    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)

    # Create logs directory if it doesn't exist
    logs_dir = Path(Path(__file__).resolve().parents[2], "logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Create file formatter
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    file_formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )

    # Create log file paths
    for file_name in (name, "default"):
        # Create log file path
        file_path = Path(logs_dir, f"{file_name}.log")
        logger.debug(f"Adding log file path: {file_path.as_posix()}")

        # Create file handler and add to logger
        file_handler = logging.FileHandler(file_path)

        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
