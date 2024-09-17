import sys
import select


def get_input():
    return input(" ").strip() + get_more_input_with_wait()


def get_more_input_with_wait(timeout=1):
    no_more_input = False
    input = ""
    while not no_more_input:
        if select.select([sys.stdin], [], [], timeout)[0]:
            input += sys.stdin.readline().strip()
        else:
            no_more_input = True
    return input
