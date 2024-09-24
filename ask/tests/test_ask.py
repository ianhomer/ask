import os
from io import StringIO
from typing import Optional
from unittest.mock import patch

from ask.bot_service import BotService

from ..ask import main, run
from .e2e_utils import create_inputter, parse_args


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
        run(inputter=create_inputter(), Service=MockBotService, parse_args=parse_args)
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert lines[1] == "OK"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3


@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_main(GenerativeModel):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = "mock-response"

    with patch("sys.stdout", new=StringIO()) as captured_output:
        main(inputter=create_inputter())
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert "mock-response" in lines[1]
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3
