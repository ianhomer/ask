from .parse import parse
import pyperclip
from typing import Optional
from rich import print


def copy_code(response_text) -> Optional[str]:
    parts = parse(response_text)
    print(
        "[bold bright_yellow]   -) code copied into clipboard [/bold bright_yellow]\n"
    )

    if len(parts) > 0:
        pyperclip.copy(parts[0][1])
    return response_text
