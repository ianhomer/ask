import os
from unittest.mock import patch
from io import StringIO
from ..ask import main
from .e2e_utils import parse_args


# Test the main entry point as used by the CLI. Other end to end tests use the
# run entry point which allows easier overrides, however it is important to have
# at least one test coming in from tha main entry point for appropriate coverage.
@patch("pyperclip.copy")
@patch("argparse.ArgumentParser")
@patch("sys.stdin", autospec=True)
@patch("prompt_toolkit.PromptSession.prompt")
@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_main(GenerativeModel, prompt, stdin, ArgumentParser, clipboard_copy):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = """
mock-response

```
const a = 1
```
"""
    prompt.side_effect = ["mock input", "copy code", "<quit>"]
    stdin.fileno.return_value = 1
    stdin.readline.return_value = "<break>"
    ArgumentParser().parse_args.return_value = parse_args()

    with patch("sys.stdout", new=StringIO()) as captured_output:
        main()
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert "mock-response" in lines[1]
        assert lines[-1] == "Bye ..."
        assert len(lines) == 7

    copies = clipboard_copy.call_args_list
    assert len(copies) == 1
    assert "const a = 1" == copies[0][0][0]
