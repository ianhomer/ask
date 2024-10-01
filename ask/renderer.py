from abc import abstractmethod
from typing import List, Optional

from rich import print
from rich.markdown import Markdown


class AbstractRenderer:
    def __init__(self, pretty_markdown=True) -> None:
        self.pretty_markdown = pretty_markdown
        self._messages: List[str] = []

    def record(self, message):
        if message and message != "\n":
            self._messages.append(message)

    @abstractmethod
    def print(self, message):
        pass

    def print_line(self, message):
        self.print(message)
        self.print("\n")

    def print_processing(self):
        self.print_line("...")

    @abstractmethod
    def print_response(self, response_text: Optional[str]):
        if response_text:
            self.print_line(response_text)

    @abstractmethod
    def print_message(self, message: str):
        self.print_line(message)

    @property
    def messages(self) -> List[str]:
        return self._messages

    @property
    def body(self) -> str:
        return "\n".join(self._messages)


class RichRenderer(AbstractRenderer):
    def print(self, message):
        print(message)

    def print_processing(self):
        self.print_line(
            "[bold bright_yellow]   -) ..."
            + "                                     ...[/bold bright_yellow]"
        )

    def print_message(self, message: str):
        self.print_line(f"[bold bright_yellow]   -) {message} [/bold bright_yellow]")

    def print_response(self, response_text: Optional[str]):
        if response_text:
            if self.pretty_markdown:
                markdown = Markdown(response_text)
                self.print_line(markdown)
            else:
                self.print_line(response_text)
