import os
from typing import Optional
from .bot_service import BotService
from llama_cpp import Llama
from .renderer import AbstractRenderer


class LlamaCpp(BotService):
    def __init__(self, prompt: str, line_target: int, renderer: AbstractRenderer):
        # self.llm = Llama.from_pretrained(
        #     repo_id="unsloth/Llama-3.2-3B-Instruct-GGUF",
        #     filename="*F16.gguf",
        #     verbose=True,
        #     n_gpu_layers=1,
        # )
        self.llm = Llama(
            model_path=os.path.expanduser(
                "~/local/models/Llama-3.2-3B-Instruct-F16.gguf"
            ),
            n_gpu_layers=-1,
        )

    @property
    def available(self) -> bool:
        return True

    def process(self, user_input: Optional[str]) -> Optional[str]:
        if user_input:
            response = self.llm(user_input, stream=False, max_tokens=512)
            return response["choices"][0]["text"]
        return None
