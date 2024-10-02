from typing import Optional

from ask.pipelines.one_shot import OneShot

from .config import default_parse_args, load_config
from .pipelines.prompt_loop import PromptLoop
from .prompt_generator import generate_prompt
from .prompter import AbstractPrompter, UserPrompter
from .quitter import Quitter
from .renderer import AbstractRenderer, RichRenderer
from .services.anthropic import AnthropicService
from .services.bot_service import BotService
from .services.gemini import Gemini
from .services.ollama import Ollama
from .transcribe import register_transcribed_text


def run(
    prompter: AbstractPrompter = UserPrompter(),
    Service: Optional[type[BotService]] = None,
    Renderer: type[AbstractRenderer] = RichRenderer,
    parse_args=default_parse_args,
    config_file_name="~/.config/ask/ask.ini",
) -> AbstractRenderer:

    config = load_config(parse_args, config_file_name)
    renderer = Renderer(pretty_markdown=config.markdown)
    quitter = Quitter(renderer)

    if config.transcribe.enabled:
        quitter.register(
            register_transcribed_text(
                config.transcribe.filename,
                prompter,
                loop_sleep=config.transcribe.loop_sleep,
            )
        )

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

    if config.pipeline == "one-shot":
        OneShot(service=service).run()
        quitter.quit(quiet=True)
    else:
        PromptLoop(
            has_initial_prompt=len(config.inputs) > 0 or file_input,
            renderer=renderer,
            quitter=quitter,
            service=service,
            prompter=prompter,
        ).run()

    return renderer


def main() -> None:
    run()
    return


if __name__ == "__main__":
    main()
