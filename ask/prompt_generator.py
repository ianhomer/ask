import os
from pathlib import Path
from typing import List, Optional, Tuple

from pypdf import PdfReader

ASK_PROMPT_DIRECTORY_NAME = "ASK_PROMPT_DIRECTORY"


def generate_prompt(inputs: List[str], template: Optional[str]) -> Tuple[str, bool]:
    parts = []
    file_input = False
    for word in inputs:
        if "." in word and os.path.exists(word):
            if word.endswith(".pdf"):
                reader = PdfReader(word)
                text = "".join(page.extract_text() for page in reader.pages)
            else:
                with open(word, "r") as file:
                    text = file.read()
            parts.append(text)
            file_input = not template
        else:
            parts.append(word)

    if template:
        if "." in template:
            prompt_file_name = template
        else:
            if ASK_PROMPT_DIRECTORY_NAME not in os.environ:
                raise Exception(
                    f"Please set {ASK_PROMPT_DIRECTORY_NAME} "
                    + "to use logical prompt names"
                )
            prompt_directory = os.environ[ASK_PROMPT_DIRECTORY_NAME]
            prompt_file_name = f"{prompt_directory}/{template}.txt"
            if not os.path.exists(prompt_file_name):
                raise Exception(f"Cannot find prompt file {prompt_file_name}")
        template = Path(prompt_file_name).read_text()
        return (template.format(*parts), file_input)
    else:
        return (" ".join(parts), file_input)
