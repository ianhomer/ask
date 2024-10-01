import os

from ..prompt_generator import generate_prompt

TESTS_DIRECTORY = os.path.dirname(__file__)


def test_generate_prompt_with_words():
    inputs = ["hello", "world"]
    assert generate_prompt(inputs, None) == ("hello world", False)


def test_generate_prompt_with_text_file():
    inputs = [f"{TESTS_DIRECTORY}/test.md"]
    assert generate_prompt(inputs, None) == (
        "# Test\n\nThis is a test file\n",
        True,
    )


def test_generate_prompt_with_pdf_file():
    inputs = [f"{TESTS_DIRECTORY}/test.pdf"]
    assert generate_prompt(inputs, None) == (
        "test\n Test\nThis is a test ﬁle",
        True,
    )


def test_generate_prompt_with_template():
    inputs = ["fish", "cat"]
    assert generate_prompt(inputs, f"{TESTS_DIRECTORY}/prompt.txt") == (
        "one fish two cat\n",
        False,
    )
