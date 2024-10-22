import argparse
import configparser
import os

empty_config = configparser.ConfigParser()

DEBUG = False

ASK_PIPELINE_VARIABLE_NAME = "ASK_PIPELINE"


def is_debug():
    return DEBUG


def create_parser():
    parser = argparse.ArgumentParser(description="Asker")

    parser.add_argument("inputs", help="Input content", nargs="*")
    parser.add_argument(
        "--one",
        help="Ask a single question expecting a single response",
        action="store_true",
    )
    parser.add_argument("--debug", help="Debug logging", action="store_true")
    parser.add_argument("--template", help="Input template")
    parser.add_argument("--provider", help="Service provider", default="Gemini")
    parser.add_argument(
        "--transcribe-filename",
        help="File name for transcribed inputs",
        default="/tmp/transcribe.txt",
    )
    parser.add_argument(
        "--transcribe-loop-sleep",
        help="Sleep time for transcribe read loop",
        default=1,
    )
    parser.add_argument(
        "--dry",
        help="Just output the prompt and then exit",
        action="store_true",
    )
    parser.add_argument("--line-target", help="Line target for output", default=0)
    parser.add_argument(
        "--no-transcribe",
        help="Disable transcribe reading",
        action="store_true",
    )
    parser.add_argument(
        "--no-markdown",
        help="Disable rendering of Markdown responses",
        action="store_true",
    )
    return parser


def default_parse_args() -> argparse.Namespace:
    return create_parser().parse_args()


def load_config(actual_parse_args, config_file_name):
    global DEBUG
    config = configparser.ConfigParser()
    config_file_path = os.path.expanduser(config_file_name)
    config.read(config_file_path)

    args = actual_parse_args()

    merged_config = Config(args, config)
    DEBUG = merged_config.debug_enabled
    return merged_config


class Config:
    def __init__(self, args, config) -> None:
        self.config = config
        self.args = args

    @property
    def service(self):
        return ServiceConfig(self.config, self.args, "service")

    @property
    def transcribe(self):
        return TranscribeConfig(self.config, self.args, "transcribe", self.pipeline)

    @property
    def markdown(self) -> bool:
        return self.config.get(
            "DEFAULT", "markdown", fallback=not self.args.no_markdown
        )

    @property
    def dry(self) -> bool:
        return self.config.get("DEFAULT", "dry", fallback=self.args.dry)

    @property
    def debug_enabled(self) -> bool:
        return self.config.get("DEFAULT", "debug", fallback=self.args.debug)

    @property
    def pipeline(self) -> str:
        if ASK_PIPELINE_VARIABLE_NAME in os.environ:
            return os.environ[ASK_PIPELINE_VARIABLE_NAME]

        pipeline = self.config.get("DEFAULT", "pipeline", fallback=None)

        if pipeline:
            return pipeline

        if self.args.one:
            return "one-shot"
        else:
            return "prompt-loop"

    @property
    def inputs(self) -> list[str]:
        return self.config.get("DEFAULT", "inputs", fallback=self.args.inputs)

    @property
    def template(self) -> str:
        return self.config.get("DEFAULT", "template", fallback=self.args.template)

    @property
    def line_target(self) -> int:
        return self.config.get("DEFAULT", "line_target", fallback=self.args.line_target)


class ServiceConfig:
    def __init__(self, config, args, section_name) -> None:
        self.section_name = section_name
        self.config = config
        self.args = args

    @property
    def model(self) -> str:
        return self.config.get(self.section_name, "model", fallback="gemini-1.5-flash")

    @property
    def provider(self) -> str:
        return self.config.get(
            self.section_name, "provider", fallback=self.args.provider
        )


class TranscribeConfig:
    def __init__(self, config, args, section_name, pipeline_name) -> None:
        self.section_name = section_name
        self.config = config
        self.args = args
        self.pipeline_name = pipeline_name

    @property
    def filename(self) -> str:
        return self.config.get(
            self.section_name,
            "filename",
            fallback=self.args.transcribe_filename,
        )

    @property
    def loop_sleep(self) -> float:
        return self.config.get(
            self.section_name,
            "loop_sleep",
            fallback=self.args.transcribe_loop_sleep,
        )

    @property
    def enabled(self) -> bool:
        if self.pipeline_name == "one-shot":
            return False
        return self.config.get(
            "DEFAULT", "enabled", fallback=not self.args.no_transcribe
        )
