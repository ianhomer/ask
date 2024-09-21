from io import StringIO
from unittest.mock import patch
import argparse
import os


from ..ask import main
from ..input import InputInterrupt


@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_gemini(GenerativeModel):
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

    mock = GenerativeModel()
    mock.start_chat().send_message().text = "mock-response"

    with patch("sys.stdout", new=StringIO()) as captured_output:
        main(inputter=get_input, parse_args=parse_args)
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert lines[1] == "mock-response"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3
