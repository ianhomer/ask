import os
from ..gemini import API_KEY_NAME

os.environ.pop(API_KEY_NAME)

assert API_KEY_NAME not in os.environ
