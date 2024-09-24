from io import StringIO
from unittest.mock import patch
import os


from ..ask import main
from .e2e_utils import parse_args, create_inputter


@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_gemini(GenerativeModel):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = "mock-response"

    with patch("sys.stdout", new=StringIO()) as captured_output:
        main(inputter=create_inputter(), parse_args=parse_args)
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert lines[1] == "mock-response"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3
