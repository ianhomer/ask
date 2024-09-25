import configparser
import os


def load_config(config_file_name="~/.config/ask/ask.ini"):
    config = configparser.ConfigParser()
    config_file_path = os.path.expanduser(config_file_name)
    config.read(config_file_path)

    return config
