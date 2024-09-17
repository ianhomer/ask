from ..transcribe import transcribe_filter


def test_not_filtered():
    assert transcribe_filter("Hello") == "Hello"

def test_square_bracket_message():
    assert not transcribe_filter("[message]")

def test_square_bracket_message_with_space():
    assert not transcribe_filter(" [message] ")

def test_round_bracket_message():
    assert not transcribe_filter("(message)")
