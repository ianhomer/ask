from abc import abstractmethod

from ..renderer import AbstractRenderer


class BotService:
    @abstractmethod
    def __init__(
        self, prompt: str, line_target: int, renderer: AbstractRenderer
    ) -> None:
        pass

    @abstractmethod
    def process(self, user_input: str) -> str:
        pass

    @property
    @abstractmethod
    def available(self) -> bool:
        pass
