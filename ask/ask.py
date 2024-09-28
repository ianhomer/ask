import signal
import threading
import sys
from typing import Optional


from .input import (
    AbstractInputter,
    InputInterrupt,
    PromptInputter,
)
from .prompt import get_prompt
from .transcribe import register_transcribed_text, stop_transcribe
from .config import load_config, default_parse_args
from .gemini import Gemini
from .anthropic import AnthropicService
from .ollama import Ollama
from .renderer import RichRenderer, AbstractRenderer
from .bot_service import BotService
from .handler import InputHandler

transcribe_thread: Optional[threading.Thread] = None


def signal_handler(sig: int, frame: Optional[object]) -> None:
    quit(RichRenderer())
    sys.exit(0)


def quit(renderer: AbstractRenderer) -> None:
    renderer.print_line("Bye ...")
    if transcribe_thread:
        stop_transcribe()


signal.signal(signal.SIGINT, signal_handler)


def run(
    inputter: AbstractInputter = PromptInputter(),
    Service: Optional[type[BotService]] = None,
    Renderer: type[AbstractRenderer] = RichRenderer,
    parse_args=default_parse_args,
    config_file_name="~/.config/ask/ask.ini"
) -> AbstractRenderer:
    global transcribe_thread

    config = load_config(parse_args, config_file_name)

    renderer = Renderer(pretty_markdown=config.markdown)
    input_handler = InputHandler(renderer=renderer)

    file_input = False

    prompt, file_input = get_prompt(config.inputs, config.template)

    if config.dry:
        renderer.print_line("Prompt : ")
        renderer.print_line(prompt)
        return renderer

    if not Service:
        match config.service.provider.lower():
            case "ollama":
                Service = Ollama
            case "anthropic":
                Service = AnthropicService
            case _:
                Service = Gemini
    service = Service(renderer=renderer, prompt=prompt, line_target=config.line_target)

    def process(user_input) -> Optional[str]:
        renderer.print_processing()
        response_text = service.process(user_input)
        renderer.print_response(response_text)
        return response_text

    response_text: Optional[str] = None

    if config.transcribe.enabled:
        transcribe_thread = register_transcribed_text(
            config.transcribe.filename,
            inputter,
            loop_sleep=config.transcribe.loop_sleep,
        )
    if config.inputs or file_input:
        response_text = process(
            "answer or do what I just asked. If you have no answer, "
            + "just say the word :'OK'",
        )

    while service.available:
        try:
            user_input = inputter.get_input()
        except InputInterrupt:
            quit(renderer)
            break
        if user_input and len(user_input) > 0:
            input_handler_response = input_handler.handle(user_input, response_text)
            if input_handler_response.quit:
                quit(renderer)
                break
            if input_handler_response.process:
                response_text = process(user_input)

    return renderer


def main() -> None:
    run()
    return


if __name__ == "__main__":
    main()
