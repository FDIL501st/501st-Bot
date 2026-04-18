from typing import TypeAlias

DEFAULT_PROMPT_TEMPLATE = "### Human:\n{0}\n\n### Assistant:\n"
MessageType: TypeAlias = 'dict[str, str]'
