from typing import TypeAlias
from llama_cpp import Llama
from nextcord.ext import commands

# DEFAULT_PROMPT_TEMPLATE = "### Human:\n{0}\n\n### Assistant:\n"
MessageType: TypeAlias = 'dict[str, str]'


# path ./ is relative to where __main__ is
llm = Llama(model_path="gemma-4-E2B-it-UD-Q4_K_XL.gguf", verbose=False, n_ctx=0, n_threads=4, n_batch=128)

# class LLM(commands.Cog):
#     def __init__(self, bot: commands.Bot) -> None:
#         super().__init__()
#         self.bot = bot
#         self.llm = llm


# def setup(bot):
#     bot.add_cog(LLM(bot))