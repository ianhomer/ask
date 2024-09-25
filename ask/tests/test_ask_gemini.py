from io import StringIO
from unittest.mock import patch
import os


from ..ask import run
from .e2e_utils import MockInputter, parse_args, CapturingRenderer


@patch("google.generativeai.GenerativeModel")
def test_ask_gemini_key_required(GenerativeModel):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = "mock-response"

    renderer = run(
        inputter=MockInputter(), Renderer=CapturingRenderer, parse_args=parse_args
    )
    assert "set in the environment variable GEMINI_API_KEY" in renderer.messages[0]
    lines = [line for line in renderer.body.split("\n") if line]
    assert len(lines) == 3


@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_gemini(GenerativeModel):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = "mock-response"

    with patch("sys.stdout", new=StringIO()) as captured_output:
        run(inputter=MockInputter(), parse_args=parse_args)
        lines = [line for line in captured_output.getvalue().split("\n") if line]
        assert lines[0] == "   -) ...                                     ..."
        assert lines[1] == "mock-response"
        assert lines[-1] == "Bye ..."
        assert len(lines) == 3


@patch("pyperclip.copy")
@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_gemini_copy_code(GenerativeModel, clipboard_copy):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = """
mock-response

```
const a = 1
```
"""

    renderer = run(
        inputter=MockInputter(inputs=["mock input 1", "copy code"]),
        Renderer=CapturingRenderer,
        parse_args=parse_args,
    )
    lines = [line for line in renderer.body.split("\n") if line]
    assert lines[0] == "..."
    assert lines[1].split("\n")[0] == "mock-response"
    assert lines[-1] == "Bye ..."
    assert len(lines) == 7

    copies = clipboard_copy.call_args_list
    assert len(copies) == 1
    assert "const a = 1" == copies[0][0][0]


@patch("google.generativeai.GenerativeModel")
@patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key"})
def test_ask_gemini_empty_inputs(GenerativeModel):
    mock = GenerativeModel()
    mock.start_chat().send_message().text = "mock-response"
    renderer = run(
        inputter=MockInputter(inputs=["mock input 1", "", "", ""]),
        Renderer=CapturingRenderer,
        parse_args=parse_args,
    )
    lines = [line for line in renderer.body.split("\n") if line]
    assert lines[0] == "..."
    assert lines[1] == "mock-response"
    assert lines[-1] == "Bye ..."
    assert len(lines) == 3
