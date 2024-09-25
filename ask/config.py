import configparser
import os

empty_config = configparser.ConfigParser()


def load_config(config_file_name="~/.config/ask/ask.ini"):
    config = configparser.ConfigParser()
    config_file_path = os.path.expanduser(config_file_name)
    config.read(config_file_path)

    return Config(config)


class Config:
    def __init__(self, config) -> None:
        self.config = config

    @property
    def service(self):
        return ServiceConfig(self.config, "service")

    @property
    def transcribe(self):
        return TranscribeConfig(self.config, "transcribe")


class ServiceConfig:
    def __init__(self, config, section_name) -> None:
        self.section_name = section_name
        self.config = config

    @property
    def model(self) -> str:
        return self.config.get(self.section_name, "model", fallback="gemini-1.5-flash")

    @property
    def provider(self) -> str:
        return self.config.get(self.section_name, "provider", fallback="Gemini")


class TranscribeConfig:
    def __init__(self, config, section_name) -> None:
        self.section_name = section_name
        self.config = config

    @property
    def filename(self) -> str:
        return self.config.get(
            self.section_name, "filename", fallback="/tmp/transcribe.txt"
        )
