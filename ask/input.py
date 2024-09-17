import sys
import select
from prompt_toolkit import PromptSession

prompt_session = PromptSession()


class InputInterrupt(KeyboardInterrupt):
    pass


def get_input():
    try:
        return prompt_session.prompt(" ").strip() + get_more_input_with_wait()
    except KeyboardInterrupt as e:
        raise InputInterrupt(e)

def get_more_input_with_wait(timeout=1):
    no_more_input = False
    input = ""
    while not no_more_input:
        if select.select([sys.stdin], [], [], timeout)[0]:
            input += sys.stdin.readline().strip()
        else:
            no_more_input = True
    return input
