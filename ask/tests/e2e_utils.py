import argparse
from collections import deque
from ..input import InputInterrupt, AbstractInputter
from ..renderer import AbstractRenderer


class MockInputter(AbstractInputter):
    def __init__(self, inputs=["mock input 1"]) -> None:
        self.queue = deque(inputs)

    def get_input(self) -> str:
        if len(self.queue) == 0:
            raise InputInterrupt()

        return self.queue.popleft()


def mock_parse_args():
    return argparse.Namespace(
        dry=False,
        inputs=[],
        line_target=0,
        transcribe_loop_sleep=0.5,
        transcribe_filename="/tmp/transcribe.txt",
        no_markdown=True,
        no_transcribe=True,
        template=None,
    )


class CapturingRenderer(AbstractRenderer):
    def __init__(self, pretty_markdown: bool) -> None:
        AbstractRenderer.__init__(self, pretty_markdown=pretty_markdown)

    def print(self, message):
        self.record(message)
