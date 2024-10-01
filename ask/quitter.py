import signal
import sys
from typing import Callable, List, Optional

from .renderer import AbstractRenderer, RichRenderer


class Quitter:
    def __init__(self, renderer: AbstractRenderer = RichRenderer()) -> None:
        self.renderer = renderer
        self.closers: List[Callable[[], None]] = []

    def register(self, closer):
        self.closers.append(closer)

    def quit(self, quiet=False):
        if not quiet:
            self.renderer.print_line("Bye ...")
        for closer in self.closers:
            closer()


def quit(quitter: Quitter) -> None:
    quitter.quit()


def signal_handler(sig: int, frame: Optional[object]) -> None:
    quit(Quitter())
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
