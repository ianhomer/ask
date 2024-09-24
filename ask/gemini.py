import os
from collections.abc import Iterable
import google.generativeai as genai
from google.generativeai.types import content_types
from typing import Optional

from ask.renderer import AbstractRenderer
from ask.service import BotService

from .save import save
from .copy import copy_code

API_KEY_NAME = "GEMINI_API_KEY"


class Gemini(BotService):
    def __init__(self, prompt, renderer: AbstractRenderer, line_target=0) -> None:
        if API_KEY_NAME not in os.environ:
            print(
                f"""

      Please get a Gemini API key from https://aistudio.google.com/
      and set in the environment variable {API_KEY_NAME}

                  """
            )
            self._available = False
            return
        self._available = True
        api_key = os.environ[API_KEY_NAME]
        self.renderer = renderer

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        history: Iterable[content_types.StrictContentType] = [
            {"role": "user", "parts": [prompt]},
            {"role": "model", "parts": ["Thanks, what would like?"]},
        ]
        if line_target:
            history += [
                {
                    "role": "user",
                    "parts": [
                        f"Unless I say otherwise keep responses below {line_target} lines"
                    ],
                },
                {"role": "model", "parts": "I understand"},
            ]
        self.chat = model.start_chat(history=history)

    @property
    def available(self) -> bool:
        return self._available

    def process_user_input(self, user_input: str) -> Optional[str]:
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            print(f"\nCannot process prompt \n{user_input}\n", e)

        return None

    def process(
        self, user_input, previous_response_text: Optional[str] = None
    ) -> Optional[str]:
        user_input_lower = user_input.lower()
        if user_input_lower == "save":
            save(previous_response_text)
            return previous_response_text

        if previous_response_text and (
            ("copy code" in user_input_lower and len(user_input) < 12)
            or ("copy" in user_input_lower and len(user_input) < 7)
        ):
            copy_code(self.renderer, previous_response_text)
            return previous_response_text

        if user_input_lower.endswith("ignore"):
            return None

        if len(user_input) > 0:
            return self.process_user_input(user_input)

        return None
