import requests

from .bot_service import BotService


class Ollama(BotService):
    @property
    def available(self) -> bool:
        return True

    def send_messaeg(self, prompt: str) -> str:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False,
            },
        )
        return response.json()["response"]
