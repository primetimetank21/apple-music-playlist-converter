import logging


def create_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    # Create logger
    logger = logging.getLogger(name)
    logging.basicConfig(
        # format="%(asctime)s\t%(levelname)-8s\t%(message)s", level=logging.DEBUG
        format="%(asctime)s\t%(levelname)-8s %(filename)s:%(lineno)d\t%(message)s",
        level=level,
    )

    return logger
