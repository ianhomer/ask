from typing import Optional

from prompt_toolkit.patch_stdout import patch_stdout

from ask.quitter import Quitter
from ask.renderer import AbstractRenderer
from ask.services.bot_service import BotService

from ..pre_processor import PromptPreProcessor
from ..prompter import AbstractPrompter, InputInterrupt
from .pipeline import Pipeline


class PromptLoop(Pipeline):
    def __init__(
        self,
        has_initial_prompt: bool,
        renderer: AbstractRenderer,
        service: BotService,
        quitter: Quitter,
        prompter: AbstractPrompter,
    ) -> None:
        self.has_initial_prompt = has_initial_prompt
        self.renderer = renderer
        self.service = service
        self.quitter = quitter
        self.prompter = prompter
        pass

    def run(self) -> None:

        prompt_pre_processor = PromptPreProcessor(renderer=self.renderer)

        response_text: Optional[str] = None

        if self.has_initial_prompt:
            response_text = self.service.send_message(
                "answer or do what I just asked. If you have no answer, "
                + "just say the word :'OK'",
            )

        while self.service.available:
            try:
                with patch_stdout():
                    prompt = self.prompter.get_input()
            except InputInterrupt:
                self.quitter.quit()
                break
            if prompt and len(prompt) > 0:
                input_handler_response = prompt_pre_processor.handle(
                    prompt, response_text
                )
                if input_handler_response.quit:
                    self.quitter.quit()
                    break
                if input_handler_response.process:
                    try:
                        response_text = self.service.process(prompt)
                    except Exception as e:
                        print(f"\nCannot process prompt \n{prompt}\n", e)
