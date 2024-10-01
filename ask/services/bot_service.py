from abc import abstractmethod

from ..renderer import AbstractRenderer


class BotService:
    @abstractmethod
    def __init__(
        self, prompt: str, renderer: AbstractRenderer, line_target: int
    ) -> None:
        self.renderer = renderer

    def process_message(self, prompt) -> str:
        response_text = self.send_message(prompt)
        self.renderer.print_response(response_text)
        return response_text

    def process(self, prompt) -> str:
        self.renderer.print_processing()
        return self.process_message(prompt)

    @abstractmethod
    def send_message(self, prompt: str) -> str:
        pass

    @property
    @abstractmethod
    def available(self) -> bool:
        pass
