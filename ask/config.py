import configparser
import os


def load_config():
    config = configparser.ConfigParser()
    config_file_path = os.path.expanduser("~/.config/ask/ask.ini")
    config.read(config_file_path)

    return config
