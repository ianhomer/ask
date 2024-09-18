from ..transcribe import transcribe_filter


def test_not_filtered():
    assert transcribe_filter("Hello") == "Hello"


def test_starred_message():
    assert not transcribe_filter("*snap*")


def test_dots_message():
    assert not transcribe_filter(".")
    assert not transcribe_filter("...")


def test_square_bracket_message():
    assert not transcribe_filter("[message]")


def test_multiple_square_bracket_messages():
    assert not transcribe_filter("[message] \n [message] ")


def test_square_bracket_message_with_space():
    assert not transcribe_filter(" [message] ")


def test_round_bracket_message():
    assert not transcribe_filter("(message)")


def test_round_bracket_message_with_spaces():
    assert not transcribe_filter(" (keyboard clacking) ")


def test_noise_words():
    assert not transcribe_filter("thank you")
    assert not transcribe_filter("thank you.")
    assert not transcribe_filter("Thank you.")


def test_dot():
    assert not transcribe_filter(".")
