import os

from ...config import load_config
from ..e2e_utils import default_parse_args_for_tests, empty_args, generate_args

TESTS_DIRECTORY = os.path.dirname(__file__)


def test_config_defaults():
    config = load_config(default_parse_args_for_tests, f"{TESTS_DIRECTORY}/empty.ini")

    assert config.service.provider == "mock"
    assert config.service.model == "gemini-1.5-flash"
    assert config.transcribe.filename == "/tmp/transcribe.txt"


def test_simple_config():
    config = load_config(empty_args, f"{TESTS_DIRECTORY}/simple.ini")

    assert config.service.provider == "Gemini"
    assert config.service.model == "gemini-1.5-flash"
    assert config.transcribe.filename == "/tmp/simple-transcribe.txt"


def test_one_shot_config():
    config = load_config(empty_args, f"{TESTS_DIRECTORY}/one-shot.ini")

    assert config.pipeline == "one-shot"


def test_one_shot_config_from_args():
    config = load_config(generate_args(["--one"]), f"{TESTS_DIRECTORY}/one-shot.ini")

    assert config.pipeline == "one-shot"
    assert not config.transcribe.enabled
