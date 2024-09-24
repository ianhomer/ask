from abc import abstractmethod
from rich import print
from typing import Optional, List
from rich.markdown import Markdown


class AbstractRenderer:
    def __init__(self, pretty_markdown=True) -> None:
        self.pretty_markdown = pretty_markdown
        self._messages: List[str] = []

    def record(self, message):
        self._messages.append(message)

    @abstractmethod
    def print(self, message):
        pass

    def print_processing(self):
        self.print("...\n")

    @abstractmethod
    def print_response(self, response_text: Optional[str]):
        if response_text:
            self.print(response_text)

    @abstractmethod
    def print_message(self, message: str):
        self.print(message)

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
        self.print(
            "[bold bright_yellow]   -) ...                                     ...[/bold bright_yellow]\n"
        )

    def print_message(self, message: str):
        self.print(f"[bold bright_yellow]   -) {message} [/bold bright_yellow]\n")

    def print_response(self, response_text: Optional[str]):
        if response_text:
            if self.pretty_markdown:
                markdown = Markdown(response_text)
                self.print(markdown)
            else:
                self.print(response_text)
