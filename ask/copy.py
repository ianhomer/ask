from .renderer import AbstractRenderer
from .parse import parse_markdown_for_code_blocks
import pyperclip


def copy_code(renderer: AbstractRenderer, response_text: str) -> None:
    parts = parse_markdown_for_code_blocks(response_text)

    if len(parts) > 0:
        renderer.print_message("code copied into clipboard")
        pyperclip.copy(parts[0][1])
