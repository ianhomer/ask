from .. import get_prompt
import os

TESTS_DIRECTORY = os.path.dirname(__file__)


def test_get_prompt_with_words():
    inputs = ["hello", "world"]
    assert get_prompt(inputs, None) == ("hello world", False)


def test_get_prompt_with_text_file():
    inputs = [f"{TESTS_DIRECTORY}/test.md"]
    assert get_prompt(inputs, None) == ("# Test\n\nThis is a test file\n", True)


def test_get_prompt_with_pdf_file():
    inputs = [f"{TESTS_DIRECTORY}/test.pdf"]
    assert get_prompt(inputs, None) == ("test\n Test\nThis is a test ﬁle", True)


def test_get_prompt_with_template():
    inputs = ["fish", "cat"]
    assert get_prompt(inputs, f"{TESTS_DIRECTORY}/prompt.txt") == (
        "one fish two cat\n",
        False,
    )
