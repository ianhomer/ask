from ask.services.bot_service import BotService

from .pipeline import Pipeline


class OneShot(Pipeline):
    def __init__(
        self,
        service: BotService,
    ) -> None:
        self.service = service
        pass

    def run(self) -> None:
        self.service.process_message("answer or do what I just asked")
