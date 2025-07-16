from contextlib import contextmanager
import re
from typing import TypeAlias, override
from os import PathLike
import warnings
from gpt4all import GPT4All

# copied following from gpt4all.py file from my .venv

DEFAULT_PROMPT_TEMPLATE = "### Human:\n{0}\n\n### Assistant:\n"
MessageType: TypeAlias = 'dict[str, str]'


gpt_model: GPT4All = GPT4All("gpt4all-falcon-newbpe-q4_0.gguf", model_path="./", device="cpu")

class MyGPT4All(GPT4All):
    """A child class to overwrite the chat_session context manager to include history."""

    def __init__(self, model_name: str, *, model_path: str | PathLike[str] | None = None, model_type: str | None = None, allow_download: bool = True, n_threads: int | None = None, device: str | None = None, n_ctx: int = 2048, ngl: int = 100, verbose: bool = False):
        super().__init__(model_name, model_path=model_path, model_type=model_type, allow_download=allow_download, n_threads=n_threads, device=device, n_ctx=n_ctx, ngl=ngl, verbose=verbose)



# gpt_model equivalent of MyGPT4All class
my_gpt_model: MyGPT4All = MyGPT4All("gpt4all-falcon-newbpe-q4_0.gguf", model_path="./", device="cpu")
