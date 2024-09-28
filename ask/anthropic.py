import os
from anthropic import Anthropic
from typing import Optional

from anthropic.types import TextBlock
from .bot_service import BotService
from .renderer import AbstractRenderer

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

    def process(self, user_input: str) -> Optional[str]:
        try:
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
        except Exception as e:
            print(f"\nCannot process prompt \n{user_input}\n", e)

        return None
