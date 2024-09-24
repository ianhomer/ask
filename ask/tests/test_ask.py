from io import StringIO
from unittest.mock import patch
from typing import Optional

from ask.service import BotService

from .e2e_utils import parse_args, create_inputter
from ..ask import main


class MockBotService(BotService):
    def process(
        self, user_input, previous_response_text: Optional[str] = None
    ) -> Optional[str]:
        return "OK"

    @property
    def available(self):
        return True


def test_ask_main():
    with patch("sys.stdout", new=StringIO()) as captured_output:
        main(
            inputter=create_inputter(), Service=MockBotService, parse_args=parse_args
        )
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert lines[1] == "OK"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3
