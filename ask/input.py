import select
import sys
from abc import abstractmethod

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.styles import Style


class InputInterrupt(KeyboardInterrupt):
    pass


style = Style.from_dict({"marker": "#FFA500 bold"})

prompt_fragments: AnyFormattedText = [("class:marker", "(-_-) ")]


class AbstractInputter:
    @abstractmethod
    def get_input(self) -> str:
        pass

    @abstractmethod
    def write(self, message: str) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def has_text(self) -> bool:
        pass

    def is_running(self) -> bool:
        return True


class PromptInputter(AbstractInputter):
    def __init__(self) -> None:
        self.prompt_session = PromptSession()

    @property
    def current_buffer(self):
        return self.prompt_session.app.current_buffer

    def get_input(self) -> str:
        try:
            return (
                self.prompt_session.prompt(prompt_fragments, style=style).strip()
                + self.get_more_input_with_wait()
            )
        except KeyboardInterrupt as e:
            raise InputInterrupt(e)

    def write(self, message: str) -> None:
        self.current_buffer.insert_text(message)

    def flush(self) -> None:
        self.current_buffer.validate_and_handle()

    def has_text(self) -> bool:
        return len(self.current_buffer.text) > 0

    def is_running(self) -> bool:
        return self.prompt_session.app.is_running

    def get_more_input_with_wait(self, timeout=1):
        no_more_input = False
        input = ""
        while not no_more_input:
            if select.select([sys.stdin], [], [], timeout)[0]:
                next_input = sys.stdin.readline().strip()
                # <break> signal is currently only used in the full end to end test
                # test_ask_main.py to indicate that we should stop processing this
                # wait.  It would be good to find a better way of doing this and
                # then remove the handling of this signal.
                if next_input == "<break>":
                    no_more_input = True
                input += next_input
            else:
                no_more_input = True
        return input
