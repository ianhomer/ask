from abc import abstractmethod
from typing import Optional


class BotService:
    @abstractmethod
    def __init__(self, prompt: str, line_target: int) -> None:
        pass

    @abstractmethod
    def process(
        self, user_input, previous_response_text: Optional[str] = None
    ) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def available(self) -> bool:
        pass
