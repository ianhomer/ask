from .parse import parse_markdown_for_code_blocks
import pyperclip
from rich import print


def copy_code(response_text: str) -> None:
    parts = parse_markdown_for_code_blocks(response_text)

    if len(parts) > 0:
        print(
            "[bold bright_yellow]   -) code copied into clipboard [/bold bright_yellow]\n"
        )
        pyperclip.copy(parts[0][1])
