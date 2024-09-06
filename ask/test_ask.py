from .ask import get_prompt


def test_get_prompt_with_words():
    inputs = ["hello", "world"]
    assert get_prompt(inputs, None) == ("hello world", False)
