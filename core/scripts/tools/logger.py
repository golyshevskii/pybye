import logging
import time

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
YELLOW_BG = "\033[43m"
BLUE_BG = "\033[44m"


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s")
    formatter.converter = time.gmtime
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger


def color_text(text: str, color_code: str) -> str:
    return f"{color_code}{text}{RESET}"
