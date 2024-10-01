from typing import Optional

from prompt_toolkit.patch_stdout import patch_stdout

from .config import default_parse_args, load_config
from .pre_processor import PromptPreProcessor
from .prompt_generator import generate_prompt
from .prompter import AbstractPrompter, InputInterrupt, UserPrompter
from .quitter import Quitter
from .renderer import AbstractRenderer, RichRenderer
from .services.anthropic import AnthropicService
from .services.bot_service import BotService
from .services.gemini import Gemini
from .services.ollama import Ollama
from .transcribe import register_transcribed_text


def run(
    inputter: AbstractPrompter = UserPrompter(),
    Service: Optional[type[BotService]] = None,
    Renderer: type[AbstractRenderer] = RichRenderer,
    parse_args=default_parse_args,
    config_file_name="~/.config/ask/ask.ini",
) -> AbstractRenderer:

    config = load_config(parse_args, config_file_name)

    renderer = Renderer(pretty_markdown=config.markdown)
    quitter = Quitter(renderer)
    prompt_pre_processor = PromptPreProcessor(renderer=renderer)

    file_input = False

    prompt, file_input = generate_prompt(config.inputs, config.template)

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

    response_text: Optional[str] = None

    if config.transcribe.enabled:
        quitter.register(
            register_transcribed_text(
                config.transcribe.filename,
                inputter,
                loop_sleep=config.transcribe.loop_sleep,
            )
        )
    if config.inputs or file_input:
        response_text = service.send_message(
            "answer or do what I just asked. If you have no answer, "
            + "just say the word :'OK'",
        )

    while service.available:
        try:
            with patch_stdout():
                prompt = inputter.get_input()
        except InputInterrupt:
            quitter.quit()
            break
        if prompt and len(prompt) > 0:
            input_handler_response = prompt_pre_processor.handle(prompt, response_text)
            if input_handler_response.quit:
                quitter.quit()
                break
            if input_handler_response.process:
                try:
                    response_text = service.process(prompt)
                except Exception as e:
                    print(f"\nCannot process prompt \n{prompt}\n", e)

    return renderer


def main() -> None:
    run()
    return


if __name__ == "__main__":
    main()
