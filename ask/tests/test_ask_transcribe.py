from typing import Optional

from ask.tests.transcribe_prompt_inputter import TranscribePromptInputter
import argparse
import os

from ask.bot_service import BotService

from ..ask import run
from .e2e_utils import CapturingRenderer

TESTS_DIRECTORY = os.path.dirname(__file__)


def create_parse_args_with_transcribe_filename(transcribe_filename):
    def parse_args():
        return argparse.Namespace(
            dry=False,
            inputs=[],
            line_target=0,
            transcribe_loop_sleep=0.001,
            no_markdown=True,
            no_transcribe=False,
            transcribe_filename=str(transcribe_filename),
            template=None,
        )

    return parse_args


class MockBotService(BotService):
    def process(
        self, user_input, previous_response_text: Optional[str] = None
    ) -> Optional[str]:
        return "OK:" + user_input

    @property
    def available(self):
        return True


def test_ask_transcribe(tmp_path):
    transcribe_filename = tmp_path / "transcribe.txt"

    renderer = run(
        inputter=TranscribePromptInputter(transcribe_filename),
        Service=MockBotService,
        Renderer=CapturingRenderer,
        parse_args=create_parse_args_with_transcribe_filename(transcribe_filename),
        config_file_name=f"{TESTS_DIRECTORY}/config/empty.ini"
    )
    assert renderer.messages[0] == "..."
    assert renderer.messages[1] == "OK:mock input 1"
    assert renderer.messages[3] == "OK: voice input 2"
    assert renderer.messages[5] == "OK:mock input 3"
    assert renderer.messages[-1] == "Bye ..."
    assert len(renderer.messages) == 7
