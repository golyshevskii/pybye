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
