from .parse import parse
import pyperclip
from typing import Optional


def copy_code(response_text) -> Optional[str]:
    parts = parse(response_text)
    if len(parts) > 0:
        pyperclip.copy(parts[0][1])
    return response_text
