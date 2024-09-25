import os
from ...config import load_config
from ..e2e_utils import mock_parse_args

TESTS_DIRECTORY = os.path.dirname(__file__)


def test_config_defaults():
    config = load_config(mock_parse_args, f"{TESTS_DIRECTORY}/empty.ini")

    assert config.service.provider == "Gemini"
    assert config.service.model == "gemini-1.5-flash"
    assert config.transcribe.filename == "/tmp/transcribe.txt"


def test_simple_config():
    config = load_config(mock_parse_args, f"{TESTS_DIRECTORY}/simple.ini")

    assert config.service.provider == "Gemini"
    assert config.service.model == "gemini-1.5-flash"
    assert config.transcribe.filename == "/tmp/simple-transcribe.txt"
