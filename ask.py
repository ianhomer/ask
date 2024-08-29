import signal
import sys
import google.generativeai as genai
import os
import argparse


def signal_handler(sig, frame):
    print("\nBye ...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description="Asker")

parser.add_argument("inputs", help="Input content", nargs="*")

args = parser.parse_args()

API_KEY_NAME = "GEMINI_API_KEY"
file_input = False

inputs = []
for word in args.inputs:
    if "." in word and os.path.exists(word):
        with open(word, "r") as file:
            inputs.append(file.read())
            file_input = True
            pass
    inputs.append(word)


def main():
    api_key = os.environ[API_KEY_NAME]
    if not api_key:
        print(f"Please set {API_KEY_NAME}")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": " AND ".join(inputs)},
            {"role": "model", "parts": "Thanks, what would like?"},
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
        response = chat.send_message(user_input)
        print(response.text)


if __name__ == "__main__":
    main()
