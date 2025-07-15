from contextlib import contextmanager
from datetime import datetime
import json
from typing import Any, NamedTuple, NoReturn, TypedDict, override, Literal
from os import PathLike
from gpt4all import GPT4All
import jinja2
from jinja2.sandbox import ImmutableSandboxedEnvironment
from ._pyllmodel import (CancellationError as CancellationError, EmbCancelCallbackType, EmbedResult as EmbedResult,
                         LLModel, ResponseCallbackType, _operator_call, empty_response_callback)

# copied following from gpt4all github (bindings/python/gpt4all.py)

# Environment setup adapted from HF transformers
@_operator_call
def _jinja_env() -> ImmutableSandboxedEnvironment:
    def raise_exception(message: str) -> NoReturn:
        raise jinja2.exceptions.TemplateError(message)

    def tojson(obj: Any, indent: int | None = None) -> str:
        return json.dumps(obj, ensure_ascii=False, indent=indent)

    def strftime_now(fmt: str) -> str:
        return datetime.now().strftime(fmt)

    env = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
    env.filters["tojson"         ] = tojson
    env.globals["raise_exception"] = raise_exception
    env.globals["strftime_now"   ] = strftime_now
    return env

class MessageType(TypedDict):
    role: str
    content: str

class ChatSession(NamedTuple):
    template: jinja2.Template
    history: list[MessageType]


gpt_model: GPT4All = GPT4All("gpt4all-falcon-newbpe-q4_0.gguf", model_path="./", device="cpu")

class MyGPT4All(GPT4All):
    """A child class to overwrite the chat_session context manager to include history."""

    def __init__(self, model_name: str, *, model_path: str | PathLike[str] | None = None, model_type: str | None = None, allow_download: bool = True, n_threads: int | None = None, device: str | None = None, n_ctx: int = 2048, ngl: int = 100, verbose: bool = False):
        super().__init__(model_name, model_path=model_path, model_type=model_type, allow_download=allow_download, n_threads=n_threads, device=device, n_ctx=n_ctx, ngl=ngl, verbose=verbose)


    @contextmanager
    @override
    def chat_session(
        self,
        system_prompt: str | Literal[False] | None = None,
        prompt_template: str | None = None,
        **kwargs
    ):
        """
        Override Context manager to insert history, so context starts with a loaded history.

        Args:
            system_message: An initial instruction for the model, None to use the model default, or False to disable. Defaults to None.
            chat_template: Jinja template for the conversation, or None to use the model default. Defaults to None.
        """

        if system_prompt is None:
            system_prompt = self.config.get("systemMessage", False)

        if prompt_template is None:
            if "name" not in self.config:
                raise ValueError("For sideloaded models or with allow_download=False, you must specify a chat template.")
            if "chatTemplate" not in self.config:
                raise NotImplementedError("This model appears to have a built-in chat template, but loading it is not "
                                        "currently implemented. Please pass a template to chat_session() directly.")
            if (tmpl := self.config["chatTemplate"]) is None:
                raise ValueError(f"The model {self.config['name']!r} does not support chat.")
            prompt_template = tmpl

        history = kwargs.get('history', [])
        if system_prompt is not False:
            history.append(MessageType(role="system", content=system_prompt)) # type: ignore
        self._chat_session = ChatSession(
            template=_jinja_env.from_string(prompt_template), # type: ignore
            history=history,
        )
        try:
            yield self
        finally:
            self._chat_session = None


# gpt_model equivalent of MyGPT4All class
my_gpt_model: MyGPT4All = MyGPT4All("gpt4all-falcon-newbpe-q4_0.gguf", model_path="./", device="cpu")
