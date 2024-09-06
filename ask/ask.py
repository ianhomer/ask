import signal
import sys
import google.generativeai as genai
import os
from pathlib import Path
from pypdf import PdfReader
import argparse
from typing import Optional, List, Tuple


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
ASK_PROMPT_DIRECTORY_NAME = "ASK_PROMPT_DIRECTORY"
file_input = False


def get_prompt(inputs: List[str], template: Optional[str]) -> Tuple[str, bool]:
    parts = []
    file_input = False
    for word in inputs:
        if "." in word and os.path.exists(word):
            if word.endswith(".pdf"):
                reader = PdfReader(word)
                text = "".join(page.extract_text() for page in reader.pages)
            else:
                with open(word, "r") as file:
                    text = file.read()
            parts.append(text)
            file_input = not template
        else:
            parts.append(word)

    if template:
        if "." in template:
            prompt_file_name = template
        else:
            if ASK_PROMPT_DIRECTORY_NAME not in os.environ:
                raise Exception(
                    f"Please set {ASK_PROMPT_DIRECTORY_NAME} to use logical prompt names"
                )
            prompt_directory = os.environ[ASK_PROMPT_DIRECTORY_NAME]
            prompt_file_name = f"{prompt_directory}/{template}.txt"
            if not os.path.exists(prompt_file_name):
                raise Exception(f"Cannot find prompt file {prompt_file_name}")
        template = Path(prompt_file_name).read_text()
        return (template.format(*parts), file_input)
    else:
        return (" ".join(parts), file_input)


prompt, file_input = get_prompt(args.inputs, args.template)

if args.dry:
    print("Prompt : ")
    print(prompt)
    sys.exit(0)


def main() -> None:
    if API_KEY_NAME not in os.environ:
        raise Exception(f"Please set {API_KEY_NAME}")
    api_key = os.environ[API_KEY_NAME]

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    history = [
        {"role": "user", "parts": prompt},
        {"role": "model", "parts": "Thanks, what would like?"},
    ]
    if args.line_target:
        history += [
            {
                "role": "user",
                "parts": f"Unless I say otherwise keep responses below {args.line_target} lines",
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
