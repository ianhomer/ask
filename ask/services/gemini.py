import os
from collections.abc import Iterable
from typing import Optional

import google.generativeai as genai
from google.generativeai.types import content_types

from ..renderer import AbstractRenderer
from .bot_service import BotService

API_KEY_NAME = "GEMINI_API_KEY"


class Gemini(BotService):
    def __init__(self, prompt, renderer: AbstractRenderer, line_target=0) -> None:
        self.renderer = renderer
        if API_KEY_NAME not in os.environ:
            self.renderer.print(
                f"""

      Please get a Gemini API key from https://aistudio.google.com/
      and set in the environment variable {API_KEY_NAME}

                  """
            )
            self._available = False
            return
        self._available = True
        api_key = os.environ[API_KEY_NAME]

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
                        "Unless I say otherwise keep responses below "
                        + f"{line_target} lines"
                    ],
                },
                {"role": "model", "parts": "I understand"},
            ]
        self.chat = model.start_chat(history=history)

    @property
    def available(self) -> bool:
        return self._available

    def process(self, user_input: Optional[str]) -> str:
        response = self.chat.send_message(user_input)
        return response.text
