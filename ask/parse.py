import re

code_block_regex = r"```([^\n]*)\n(.*?)\n```"


def parse(response_text):
    code_blocks = re.findall(code_block_regex, response_text, re.DOTALL)
    return code_blocks
