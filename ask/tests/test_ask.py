from io import StringIO
from unittest.mock import patch
from typing import Optional
import argparse

from ask.service import BotService

from ..ask import main
from ..input import InputInterrupt


class MockBotService(BotService):
    def process(
        self, user_input, previous_response_text: Optional[str] = None
    ) -> Optional[str]:
        return "OK"


def test_ask_main():
    inputs = ["what is 1 + 1"]

    def get_input():
        if len(inputs) == 0:
            raise InputInterrupt()

        return inputs.pop()

    def parse_args():
        return argparse.Namespace(
            dry=False,
            inputs=[],
            line_target=0,
            no_markdown=True,
            no_transcribe=True,
            template=None,
        )

    with patch("sys.stdout", new=StringIO()) as captured_output:
        main(inputter=get_input, Service=MockBotService, parse_args=parse_args)
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "OK"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 2
