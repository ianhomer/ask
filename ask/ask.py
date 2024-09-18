import argparse
import os
import signal
import sys
import threading
from collections.abc import Iterable
from typing import Optional

import google.generativeai as genai
from google.generativeai.types import content_types
from rich import print
from rich.markdown import Markdown

from .input import (
    InputInterrupt,
    get_input,
)
from .prompt import get_prompt
from .save import save
from .transcribe import register_transcribed_text, stop_transcribe
from .config import load_config

transcribe_thread: Optional[threading.Thread] = None

config = load_config()


def signal_handler(sig: int, frame: Optional[object]) -> None:
    quit()


def quit() -> None:
    print("\nBye ...")
    if transcribe_thread:
        stop_transcribe()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description="Asker")

parser.add_argument("inputs", help="Input content", nargs="*")
parser.add_argument("--template", help="Input template")
parser.add_argument(
    "--dry", help="Just output the prompt and then exit", action="store_true"
)
parser.add_argument("--line-target", help="Line target for output")
parser.add_argument(
    "--no-transcribe", help="Disable transcribe reading", action="store_true"
)


args = parser.parse_args()

API_KEY_NAME = "GEMINI_API_KEY"
file_input = False

prompt, file_input = get_prompt(args.inputs, args.template)

if args.dry:
    print("Prompt : ")
    print(prompt)
    sys.exit(0)


def process_user_input(chat, user_input: str) -> None:
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


transcribe_filename = config.get(
    "transcribe", "filename", fallback="/tmp/transcribe.txt"
)


def main() -> None:
    global transcribe_thread
    if API_KEY_NAME not in os.environ:
        print(
            f"""

  Please get a Gemini API key from https://aistudio.google.com/
  and set in the environment variable {API_KEY_NAME}

              """
        )
        sys.exit(1)
    api_key = os.environ[API_KEY_NAME]

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    history: Iterable[content_types.StrictContentType] = [
        {"role": "user", "parts": [prompt]},
        {"role": "model", "parts": ["Thanks, what would like?"]},
    ]
    if args.line_target:
        history += [
            {
                "role": "user",
                "parts": [
                    f"Unless I say otherwise keep responses below {args.line_target} lines"
                ],
            },
            {"role": "model", "parts": "I understand"},
        ]
    chat = model.start_chat(history=history)

    response_text = ""
    if not args.no_transcribe:
        transcribe_thread = register_transcribed_text(transcribe_filename)
    if args.inputs or file_input:
        process_user_input(
            chat,
            "answer or do what I just asked. If you have no answer, just say the word :'OK'",
        )

    while True:
        try:
            user_input = get_input()
        except InputInterrupt:
            quit()
            break

        if user_input.lower() == "save":
            save(response_text)
            continue

        if user_input.lower().endswith("ignore"):
            continue

        if len(user_input) > 0:
            process_user_input(chat, user_input)


if __name__ == "__main__":
    main()
