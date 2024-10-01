from io import StringIO
from typing import Optional
from unittest.mock import patch

from ..ask import run
from ..services.bot_service import BotService
from .e2e_utils import MockPrompter, mock_parse_args


class MockBotService(BotService):
    def send_message(self, prompt, previous_response_text: Optional[str] = None) -> str:
        return "OK"

    @property
    def available(self):
        return True


def test_ask_run():
    with patch("sys.stdout", new=StringIO()) as captured_output:
        run(
            prompter=MockPrompter(),
            Service=MockBotService,
            parse_args=mock_parse_args,
        )
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert lines[1] == "OK"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3
