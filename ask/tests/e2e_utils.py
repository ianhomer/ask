import argparse
from collections import deque
from typing import List

from ..config import create_parser
from ..prompter import AbstractPrompter, InputInterrupt
from ..renderer import AbstractRenderer


class MockInputter(AbstractPrompter):
    def __init__(self, inputs=["mock input 1"]) -> None:
        self.queue = deque(inputs)

    def get_input(self) -> str:
        if len(self.queue) == 0:
            raise InputInterrupt()

        return self.queue.popleft()


def mock_parse_args():
    return argparse.Namespace(
        debug=True,
        dry=False,
        inputs=[],
        line_target=0,
        no_markdown=True,
        no_transcribe=True,
        one=False,
        provider="mock",
        template=None,
        transcribe_filename="/tmp/transcribe.txt",
        transcribe_loop_sleep=0.5,
    )


def generate_args(args: List[str]):
    return lambda: create_parser().parse_args(args)


def empty_args():
    return generate_args([])()


def default_parse_args_for_tests():
    return generate_args(["--no-markdown", "--provider=mock"])()


class CapturingRenderer(AbstractRenderer):
    def __init__(self, pretty_markdown: bool) -> None:
        AbstractRenderer.__init__(self, pretty_markdown=pretty_markdown)

    def print(self, message):
        self.record(message)
