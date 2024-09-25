import time
from collections import deque

from prompt_toolkit import PromptSession

from ..input import AbstractInputter, InputInterrupt
from ..transcribe import is_running


class TranscribePromptInputter(AbstractInputter):
    def __init__(
        self,
        transcribe_filename,
        inputs=["mock input 1", "<transcribed>input 2", "mock input 3"],
    ) -> None:
        self.prompt_session = PromptSession()
        self.transcribe_filename = transcribe_filename
        self.queue = deque(inputs)

        open(transcribe_filename, "a").close()
        print(transcribe_filename)

    def get_raw_input(self) -> str:
        if len(self.queue) == 0:
            raise InputInterrupt()

        return self.queue.popleft()

    def get_input(self) -> str:
        while not is_running():
            print(str(is_running()))
            time.sleep(0.1)
        input = self.get_raw_input()
        while input.startswith("<transcribed>"):
            message = input.split(">")[1]
            with open(self.transcribe_filename, "a") as transcribe_file:
                transcribe_file.write(f"voice {message}\n")
            # Sleep for enough time for the transcribe read loop to run
            time.sleep(0.005)
            input = self.get_raw_input()
        return input

    def write(self, message: str) -> None:
        self.queue.appendleft(message)
