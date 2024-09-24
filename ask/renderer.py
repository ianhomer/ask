from abc import abstractmethod
from rich import print
from typing import Optional
from rich.markdown import Markdown


class AbstractRenderer:
    @abstractmethod
    def __init__(self, pretty_markdown: bool) -> None:
        pass

    @abstractmethod
    def print_processing(self):
        pass

    @abstractmethod
    def print_response(self, response_text: Optional[str]):
        pass

    @abstractmethod
    def print_message(self, message: str):
        pass


class RichRenderer(AbstractRenderer):
    def __init__(self, pretty_markdown=True) -> None:
        self.pretty_markdown = pretty_markdown

    def print_processing(self):
        print(
            "[bold bright_yellow]   -) ...                                     ...[/bold bright_yellow]\n"
        )

    def print_message(self, message: str):
        print(f"[bold bright_yellow]   -) {message} [/bold bright_yellow]\n")

    def print_response(self, response_text: Optional[str]):
        if response_text:
            if self.pretty_markdown:
                markdown = Markdown(response_text)
                print(markdown)
            else:
                print(response_text)
