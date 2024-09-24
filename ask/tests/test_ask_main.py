import os
from unittest.mock import patch
from io import StringIO
from ..ask import main
from .e2e_utils import parse_args


@patch("argparse.ArgumentParser")
@patch("sys.stdin", autospec=True)
@patch("prompt_toolkit.PromptSession.prompt")
@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_main(GenerativeModel, prompt, stdin, ArgumentParser):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = "mock-response"
    prompt.return_value = "quit"
    stdin.fileno.return_value = 1
    stdin.readline.return_value = "quit"
    ArgumentParser().parse_args.return_value = parse_args()

    with patch("sys.stdout", new=StringIO()) as captured_output:
        main()
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[-1] == "Bye ..."
        assert len(lines) == 1
