import argparse
from typing import Callable
from ..input import InputInterrupt


def create_inputter() -> Callable[[], str]:
    inputs = ["mock input 1"]

    def get_input() -> str:
        if len(inputs) == 0:
            raise InputInterrupt()

        return inputs.pop()

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
