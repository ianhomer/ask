import os

from ask.config import ASK_PIPELINE_VARIABLE_NAME

from ..services.anthropic import ANTHROPIC_API_KEY_NAME
from ..services.gemini import API_KEY_NAME

# Safety check to ensure that API_KEY and other environment names are not passed
# into unit tests since this could have unintended side effect from environment
# leaking in
if API_KEY_NAME in os.environ:
    os.environ.pop(API_KEY_NAME)
if ANTHROPIC_API_KEY_NAME in os.environ:
    os.environ.pop(ANTHROPIC_API_KEY_NAME)
if ASK_PIPELINE_VARIABLE_NAME in os.environ:
    os.environ.pop(ASK_PIPELINE_VARIABLE_NAME)

assert ANTHROPIC_API_KEY_NAME not in os.environ
assert API_KEY_NAME not in os.environ
assert ASK_PIPELINE_VARIABLE_NAME not in os.environ
