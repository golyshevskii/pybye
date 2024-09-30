import logging
import time

ESC = "\x1b"
RESET = f"{ESC}[0m"
ANSI_COLORS = {
    "fg": {
        "green": f"{ESC}[1;38;5;47m",
        "pink": f"{ESC}[1;38;5;219m",
        "lime": f"{ESC}[1;38;5;154m",
        "red": f"{ESC}[1;38;5;197m",
        "violet": f"{ESC}[1;38;5;135m",
        "yellow": f"{ESC}[1;38;5;227m",
    },
    "bg": {
        "green": f"{ESC}[1;48;5;47m",
        "pink": f"{ESC}[1;48;5;219m",
        "lime": f"{ESC}[1;48;5;154m",
        "red": f"{ESC}[1;48;5;197m",
        "violet": f"{ESC}[1;48;5;135m",
        "yellow": f"{ESC}[1;48;5;227m",
        "pp": f"{ESC}[1;48;5;207m",
    },
    "reset": RESET,
}


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
