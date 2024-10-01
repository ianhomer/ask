import os
from ..services.gemini import API_KEY_NAME
from ..services.anthropic import ANTHROPIC_API_KEY_NAME

# Safety check to ensure that API_KEY is not passed into unit tests since this
# could have unintended side effect from environment leaking in
if API_KEY_NAME in os.environ:
    os.environ.pop(API_KEY_NAME)
if ANTHROPIC_API_KEY_NAME in os.environ:
    os.environ.pop(ANTHROPIC_API_KEY_NAME)

assert API_KEY_NAME not in os.environ
assert ANTHROPIC_API_KEY_NAME not in os.environ
