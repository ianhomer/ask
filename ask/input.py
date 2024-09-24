import sys
import select
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.styles import Style

prompt_session: PromptSession = PromptSession()


class InputInterrupt(KeyboardInterrupt):
    pass


style = Style.from_dict({"marker": "#FFA500 bold"})

prompt_fragments: AnyFormattedText = [("class:marker", "(-_-) ")]


def get_input() -> str:
    try:
        return (
            prompt_session.prompt(prompt_fragments, style=style).strip()
            + get_more_input_with_wait()
        )
    except KeyboardInterrupt as e:
        raise InputInterrupt(e)


def get_more_input_with_wait(timeout=1):
    no_more_input = False
    input = ""
    while not no_more_input:
        if select.select([sys.stdin], [], [], timeout)[0]:
            next_input = sys.stdin.readline().strip()
            # <break> signal is currently only used in the full end to end test
            # test_ask_main.py to indicate that we should stop processing this
            # wait.  It would be good to find a better way of doing this and
            # then remove the handling of this signal.
            if next_input == "<break>":
                no_more_input = True
            input += next_input
        else:
            no_more_input = True
    return input
