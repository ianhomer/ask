import google.generativeai as genai
import os


def main():
    api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat()
    while True:
        user_input = input("(-_-) ")
        response = chat.send_message(user_input)
        print(response.text)


if __name__ == "__main__":
    main()
