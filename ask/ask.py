import argparse
import signal
import threading
from typing import Optional, Callable


from .input import (
    InputInterrupt,
    get_input,
)
from .prompt import get_prompt
from .transcribe import register_transcribed_text, stop_transcribe
from .config import load_config
from .gemini import Gemini
from .renderer import RichRenderer, AbstractRenderer
from .service import BotService

transcribe_thread: Optional[threading.Thread] = None

config = load_config()


def signal_handler(sig: int, frame: Optional[object]) -> None:
    quit()


def quit() -> None:
    print("\nBye ...")
    if transcribe_thread:
        stop_transcribe()


signal.signal(signal.SIGINT, signal_handler)


transcribe_filename = config.get(
    "transcribe", "filename", fallback="/tmp/transcribe.txt"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Asker")

    parser.add_argument("inputs", help="Input content", nargs="*")
    parser.add_argument("--template", help="Input template")
    parser.add_argument(
        "--dry", help="Just output the prompt and then exit", action="store_true"
    )
    parser.add_argument("--line-target", help="Line target for output", default=0)
    parser.add_argument(
        "--no-transcribe", help="Disable transcribe reading", action="store_true"
    )
    parser.add_argument(
        "--no-markdown",
        help="Disable rendering of Markdown responses",
        action="store_true",
    )

    return parser.parse_args()


def main(
    inputter: Callable[[], str] = get_input,
    Service: type[BotService] = Gemini,
    Renderer: type[AbstractRenderer] = RichRenderer,
    parse_args=parse_args,
) -> None:
    global transcribe_thread
    args = parse_args()

    renderer = Renderer(pretty_markdown=not args.no_markdown)

    file_input = False

    prompt, file_input = get_prompt(args.inputs, args.template)

    if args.dry:
        print("Prompt : ")
        print(prompt)
        return

    service = Service(renderer=renderer, prompt=prompt, line_target=args.line_target)

    def process(user_input, response_text: Optional[str] = None) -> Optional[str]:
        renderer.print_processing()
        response_text = service.process(user_input, response_text)
        renderer.print_response(response_text)
        return response_text

    response_text: Optional[str] = None

    if not args.no_transcribe:
        transcribe_thread = register_transcribed_text(transcribe_filename)
    if args.inputs or file_input:
        response_text = process(
            "answer or do what I just asked. If you have no answer, "
            + "just say the word :'OK'",
        )

    while service.available:
        try:
            user_input = inputter()
        except InputInterrupt:
            quit()
            break

        response_text = process(user_input, response_text)


if __name__ == "__main__":
    main()
