from typing import Optional

import requests

from .bot_service import BotService


class Ollama(BotService):
    @property
    def available(self) -> bool:
        return True

    def process(self, user_input: str) -> Optional[str]:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": user_input,
                "stream": False,
            },
        )
        return response.json()["response"]
