ESC = "\x1b"
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
    "reset": f"{ESC}[0m",
}

print(ANSI_COLORS["fg"]["green"], "BREAKOUT", ANSI_COLORS["reset"])
