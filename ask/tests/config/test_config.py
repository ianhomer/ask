import os
from ...config import load_config

TESTS_DIRECTORY = os.path.dirname(__file__)


def test_simple_config():
    config = load_config(f"{TESTS_DIRECTORY}/simple.ini")

    assert config.get("transcribe", "filename") == "/tmp/simple-transcribe.txt"
