import json
from typing import Any, Dict, Union


def read_file(path: str, is_json: bool = False) -> Union[str, Dict[str, Any]]:
    """
    Reads a file and returns its content.

    Params:
        path: The path to the file.
        is_json: Whether the file is JSON or not.
    """
    with open(path, "r", encoding="utf-8") as file:
        if is_json:
            return json.load(file)
        return file.read()


def write_file(path: str, content: Union[str, Dict[str, Any]], mode: str = "w") -> None:
    """
    Writes content to a file.

    Params:
        path: The path to the file.
        content: The content to write to the file.
    """
    with open(path, mode, encoding="utf-8") as file:
        file.write(content)
