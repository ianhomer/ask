import signal
import sys
import google.generativeai as genai
import os
from pathlib import Path
import argparse


def signal_handler(sig, frame):
    print("\nBye ...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description="Asker")

parser.add_argument("inputs", help="Input content", nargs="*")
parser.add_argument("--template", help="Input template")
parser.add_argument(
    "--dry", help="Just output the prompt and then exit", action="store_true"
)

args = parser.parse_args()

API_KEY_NAME = "GEMINI_API_KEY"
ASK_PROMPT_DIRECTORY_NAME = "ASK_PROMPT_DIRECTORY"
file_input = False


inputs = []
for word in args.inputs:
    if "." in word and os.path.exists(word):
        with open(word, "r") as file:
            inputs.append(file.read())
            file_input = True
            pass
    inputs.append(word)


if args.template:
    if "." in args.template:
        prompt_file_name = args.template
    else:
        if ASK_PROMPT_DIRECTORY_NAME not in os.environ:
            raise Exception(
                f"Please set {ASK_PROMPT_DIRECTORY_NAME} to use logical prompt names"
            )
        prompt_directory = os.environ[ASK_PROMPT_DIRECTORY_NAME]
        prompt_file_name = f"{prompt_directory}/{args.template}.txt"
        if not os.path.exists(prompt_file_name):
            raise Exception(f"Cannot find prompt file {prompt_file_name}")
    template = Path(prompt_file_name).read_text()
    prompt = template.format(*inputs)
else:
    prompt = " ".join(inputs)

if args.dry:
    print("Prompt : ")
    print(prompt)
    sys.exit(0)


def main():
    if API_KEY_NAME not in os.environ:
        raise Exception(f"Please set {API_KEY_NAME}")
    api_key = os.environ[API_KEY_NAME]

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": prompt},
            {"role": "model", "parts": "Thanks, what would like?"},
            {
                "role": "user",
                "parts": "Unless I say otherwise keep responses below 15 lines",
            },
            {"role": "model", "parts": "I understand"},
        ]
    )
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
