import logging
import time


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s")
    formatter.converter = time.gmtime
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
