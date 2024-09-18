from rich.markdown import Markdown
from typing import Optional
import google.generativeai as genai
from rich import print

from .save import save


def process_user_input(chat: genai.ChatSession, user_input: str) -> None:
    try:
        print(
            "[bold bright_yellow]   -) ...                                     ...[/bold bright_yellow]\n"
        )
        response = chat.send_message(user_input)
        response_text = response.text
        markdown = Markdown(response_text)
        print(markdown)
    except Exception as e:
        print(f"\nCannot process prompt \n{user_input}\n", e)


def process(chat, user_input, previous_response_text) -> Optional[str]:
    if user_input.lower() == "save":
        save(previous_response_text)
        return previous_response_text

    if user_input.lower().endswith("ignore"):
        return None

    if len(user_input) > 0:
        return process_user_input(chat, user_input)

    return None
