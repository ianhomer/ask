import os

from anthropic import Anthropic
from anthropic.types import TextBlock

from ..renderer import AbstractRenderer
from .bot_service import BotService

ANTHROPIC_API_KEY_NAME = "ANTHROPIC_API_KEY"


class AnthropicService(BotService):
    def __init__(self, prompt, renderer: AbstractRenderer, line_target=0) -> None:
        self.renderer = renderer
        if ANTHROPIC_API_KEY_NAME not in os.environ:
            self.renderer.print(
                f"""

      Please get a Anthropic API key from https://console.anthropic.com/
      and set in the environment variable {ANTHROPIC_API_KEY_NAME}

                  """
            )
            self._available = False
            return
        self._available = True

        self.client = Anthropic(
            api_key=os.environ.get(ANTHROPIC_API_KEY_NAME),
        )
        self._available = True

    @property
    def available(self) -> bool:
        return self._available

    def process(self, user_input: str) -> str:
        message = self.client.messages.create(
            max_tokens=4906,
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="claude-3-5-sonnet-20240620",
        )
        content = message.content[0]
        if type(content) is TextBlock:
            return content.text
        else:
            return str(content)
