from typing import Optional

from .copy import copy_code
from .renderer import AbstractRenderer
from .save import save


class PromptPreProcessorResponse:
    def __init__(self, ignore=False, process=True, quit=False) -> None:
        self._ignore = ignore
        self._process = process
        self._quit = quit

    @property
    def ignore(self):
        return self._ignore

    @property
    def process(self):
        return self._process

    @property
    def quit(self):
        return self._quit

    def __str__(self) -> str:
        return f"ignore:{self._ignore}, process:{self._process}, quit:{self._quit}"


class PromptPreProcessor:
    def __init__(self, renderer: AbstractRenderer) -> None:
        self.renderer = renderer

    def handle(
        self, input: str, previous_response_text: Optional[str]
    ) -> PromptPreProcessorResponse:
        input_lower = input.lower()
        if input_lower == "save":
            save(previous_response_text)
            return PromptPreProcessorResponse(process=False)

        if previous_response_text and (
            ("copy code" in input_lower and len(input) < 17)
            or ("copy" in input_lower and len(input) < 7)
        ):
            copy_code(self.renderer, previous_response_text)
            return PromptPreProcessorResponse(process=False)

        # The handling for <quit> is currently only used within end to end
        # tests and may be removed.
        if (
            input_lower == "quit"
            or input_lower.endswith("<quit>")
            or input_lower.startswith("<quit>")
        ):
            return PromptPreProcessorResponse(quit=True)

        if input_lower.endswith("ignore"):
            return PromptPreProcessorResponse(process=False, ignore=True)

        return PromptPreProcessorResponse()
