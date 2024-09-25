from io import StringIO
from typing import Optional
from unittest.mock import patch

from ask.bot_service import BotService

from ..ask import run
from .e2e_utils import MockInputter, parse_args


class MockBotService(BotService):
    def process(
        self, user_input, previous_response_text: Optional[str] = None
    ) -> Optional[str]:
        return "OK"

    @property
    def available(self):
        return True


def test_ask_run():
    with patch("sys.stdout", new=StringIO()) as captured_output:
        run(inputter=MockInputter(), Service=MockBotService, parse_args=parse_args)
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert lines[1] == "OK"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3
