import os
from ..gemini import API_KEY_NAME

# Safety check to ensure that API_KEY is not passed into unit tests since this
# could have unintended side effect from environment leaking in
if API_KEY_NAME in os.environ:
    os.environ.pop(API_KEY_NAME)

assert API_KEY_NAME not in os.environ
