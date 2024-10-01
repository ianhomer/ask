import queue
import signal
import sys
import threading
from queue import Queue
from typing import List, Optional

from prompt_toolkit.patch_stdout import patch_stdout

from .config import default_parse_args, load_config
from .handler import InputHandler
from .input import AbstractInputter, InputInterrupt, PromptInputter
from .prompt import get_prompt
from .renderer import AbstractRenderer, RichRenderer
from .services.anthropic import AnthropicService
from .services.bot_service import BotService
from .services.gemini import Gemini
from .services.ollama import Ollama
from .transcribe import register_transcribed_text, stop_transcribe

transcribe_thread: Optional[threading.Thread] = None
running = True


def signal_handler(sig: int, frame: Optional[object]) -> None:
    quit(RichRenderer())
    sys.exit(0)


user_inputs: Queue[str] = queue.Queue()


def quit(renderer: AbstractRenderer) -> None:
    global running
    renderer.print_line("Bye ...")
    running = False
    user_inputs.put("")
    if transcribe_thread:
        stop_transcribe()


signal.signal(signal.SIGINT, signal_handler)


def run(
    inputter: AbstractInputter = PromptInputter(),
    Service: Optional[type[BotService]] = None,
    Renderer: type[AbstractRenderer] = RichRenderer,
    parse_args=default_parse_args,
    config_file_name="~/.config/ask/ask.ini",
) -> AbstractRenderer:
    global transcribe_thread, running

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

    def process(user_input) -> str:
        renderer.print_processing()
        response_text = service.process(user_input)
        renderer.print_response(response_text)
        return response_text

    if config.transcribe.enabled:
        transcribe_thread = register_transcribed_text(
            config.transcribe.filename,
            inputter,
            loop_sleep=config.transcribe.loop_sleep,
        )

    response_history: List[Optional[str]] = [None]

    if config.inputs or file_input:
        response_history[0] = process(
            "answer or do what I just asked. If you have no answer, "
            + "just say the word :'OK'",
        )

    def input_process():
        global running
        while running:
            try:
                with patch_stdout():
                    user_input = inputter.get_input()
            except InputInterrupt:
                quit(renderer)
                break
            if user_input and len(user_input) > 0:
                input_handler_response = input_handler.handle(
                    user_input,
                    response_history[0],
                )
                if input_handler_response.quit:
                    quit(renderer)
                    break
                user_inputs.put(user_input)

    input_thread = threading.Thread(
        target=input_process,
        args=(),
    )
    input_thread.start()
    while running and service.available:
        user_input = user_inputs.get()
        if len(user_input) > 0:
            try:
                response_history[0] = process(user_input)
            except Exception as e:
                print(f"\nCannot process prompt \n{user_input}\n", e)

    return renderer


def main() -> None:
    run()
    return


if __name__ == "__main__":
    main()
