import signal
import sys
import google.generativeai as genai
from google.generativeai.types import content_types
import os
import argparse
from typing import Optional
from collections.abc import Iterable

from get_prompt import get_prompt


def signal_handler(sig: int, frame: Optional[object]) -> None:
    print("\nBye ...")
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


def main() -> None:
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
    while True:
        user_input = (
            input("(-_-) ")
            or (
                file_input
                and "Proof read what I just gave you and tell me how to improve"
            )
            or (args.inputs and "answer what I just asked")
            or "you start"
        )
        assert user_input
        response = chat.send_message(user_input)
        print(response.text)


if __name__ == "__main__":
    main()
