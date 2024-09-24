import argparse
from typing import Callable
from collections import deque
from ..input import InputInterrupt


def create_inputter(inputs=["mock input 1"]) -> Callable[[], str]:
    queue = deque(inputs)

    def get_input() -> str:
        if len(queue) == 0:
            raise InputInterrupt()

        return queue.popleft()

    return get_input


def parse_args():
    return argparse.Namespace(
        dry=False,
        inputs=[],
        line_target=0,
        no_markdown=True,
        no_transcribe=True,
        template=None,
    )
