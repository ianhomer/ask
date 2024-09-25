from typing import Optional
from .bot_service import BotService
import requests


class Ollama(BotService):
    @property
    def available(self) -> bool:
        return True

    def process(self, user_input: Optional[str]) -> Optional[str]:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "qwen2.5:7b", "prompt": user_input, "stream": False},
        )
        return response.json()["response"]
