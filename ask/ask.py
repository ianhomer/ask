import signal
import sys
import google.generativeai as genai
from google.generativeai.types import content_types
import os
import argparse
from typing import Optional
from collections.abc import Iterable
from rich import print
from rich.markdown import Markdown
import threading

from .prompt import get_prompt
from .input import get_more_input_with_wait
from .save import save
from .transcribe import register_transcribed_text, stop_transcribe


transcribe_thread: Optional[threading.Thread] = None


def signal_handler(sig: int, frame: Optional[object]) -> None:
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






transcribe_filename = "/tmp/transcribe.txt"


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
    transcribe_thread = register_transcribed_text(transcribe_filename)
    while True:
        print("[bold orange3](-_-)[/bold orange3]", end="")
        user_input = (
            input(" ")
            or (
                file_input
                and "Proof read what I just gave you and tell me how to improve"
            )
            or (args.inputs and "answer what I just asked")
            or "you start"
        ).strip()
        user_input += get_more_input_with_wait()

        if user_input.lower() == "save":
            save(response_text)
            continue

        if user_input.lower().endswith("ignore"):
            continue

        if len(user_input) > 0:
            process_user_input(chat, user_input)


if __name__ == "__main__":
    main()
