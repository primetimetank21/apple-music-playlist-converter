import logging
from pathlib import Path
from typing import Union

LOG_DIR: Path = Path(Path.cwd(), "logs")


def create_logger(
    name: str, level: int = logging.DEBUG, log_path: Union[Path, str] = LOG_DIR
) -> logging.Logger:
    # Create logger
    logger = logging.getLogger(name)

    if isinstance(log_path, str):
        log_path = Path(log_path)

    log_path.mkdir(exist_ok=True, parents=True)

    filename: Path = Path(log_path, f"{name}.log")

    logging.basicConfig(
        format="%(asctime)s\t%(levelname)-8s %(filename)s:%(lineno)d\t%(message)s",
        level=level,
        handlers=[logging.FileHandler(filename=filename), logging.StreamHandler()],
    )

    return logger
