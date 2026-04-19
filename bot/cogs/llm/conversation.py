import asyncio
import os
import threading
import nextcord
from nextcord.ext import commands
from bot.shared.constants import CLUB_SERVER_ID, BOT_ID, CLUB_SERVER_BOT_CHANNEL
from bot.shared.model import MessageType
from collections import deque
from pprint import pformat
from llama_cpp import Llama
from bot.shared.model import llm


DEV: bool = bool(os.environ.get("DEV", "False"))

CONVERSATION_SYSTEM_PROMPT = """
You are a helpful Assistant. Your name is BB-501.
All your responses will be within 100 words.
You are permitted to talk about your true nature as a LLM.
"""

SYSTEM_PROMPT_MESSAGE: MessageType = {"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}

# path ./ is relative to where __main__ is
# llm = Llama(model_path="gemma-4-E2B-it-UD-Q4_K_XL.gguf", verbose=False, n_ctx=2048)

class ConversationBot:
    def __init__(self, model: Llama) -> None:
        self.model = model
        self.history: deque[MessageType] = deque([SYSTEM_PROMPT_MESSAGE], maxlen=21)
        # first element at all times needs to be SYSTEM_PROMPT_MESSAGE

        # maxlen takes care of automatically removing from other side
        # this gives us a context of last 20 messages with bot
        # need 1 extra space for SYSTEM_PROMPT_MESSAGE

        self._lock = threading.Lock()


    def reply(self, message: str) -> str:
        """
        Generates a reply to the message, using a llm model.
        If already busy generating, ignore the request by sending a RuntimeError.
        Will not queue for the model.

        This functional also handles history, meaning it will add the user prompt and response generated to the history.
        """

        if self._lock.acquire(blocking=False):
            try:
                # add message to history
                self.history.append({"role": "user", "content": message})
                reply = llm.create_chat_completion(messages = list(self.history), max_tokens=200, temperature=1.0, top_p=0.95, top_k=64)
                # add reply to history as well
                self.history.append(reply["choices"][0]["message"])

                return reply["choices"][0]["message"]["content"]
            finally:
                # finally block runs before return in try
                self._lock.release()
        else:
            raise RuntimeError("Conversation bot not available, currently working on generating another response.")



class Conversation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot: commands.Bot = bot
        self.conversationBot: ConversationBot = ConversationBot(llm)


    @commands.command(alias=["clear_context", "clear_history"])
    async def clear(self, ctx: commands.Context):
        """
        Clears bot history/context. Useful to start new conversations and fixing bot if it gets stuck saying same message.
        """
        self.conversationBot.history = deque([SYSTEM_PROMPT_MESSAGE], maxlen=21)
        await ctx.send("Cleared bot chat history.")

    @commands.command(alias=["view_context", "view_history"])
    async def history(self, ctx: commands.Context):
        """
        View the history/context for the bot
        """
        await ctx.send(pformat(self.conversationBot.history))

    @commands.Cog.listener('on_message')
    async def handle_listener(self, message: nextcord.Message):
        try:
            # Any message sent to just you(hidden messages) don't have a guild association
            # aka emphemeral message

            if message.guild is None:
                return # do nothing as was unable to find guild from message
            
            # can remove this if later if wanted, for now only occur within club server
            # also only for messages not by the bot (don't want bot endlessly talking to itself)
            # and for now only in the club server bot channel
            # and ignore command prefixes
            if message.guild.id == CLUB_SERVER_ID and message.author.id != BOT_ID and message.channel.id == CLUB_SERVER_BOT_CHANNEL and not message.content.startswith('./'):            
                print(f"{self.conversationBot.history}")

                # for now need to use model to reply to message
                async with message.channel.typing():
                    reply_coro = asyncio.to_thread(self.conversationBot.reply, message.content)

                    # give bot 30s think time
                    await asyncio.sleep(30)     # don't think this is working to keep typing indicator active for 30s

                    reply = await reply_coro
                
                    # reply_coro takes care of adding the promp and resopnse to its history

                    # add system_prompt to front again (it wcould be removed if our deque reached its max capacity)
                    self.conversationBot.history.popleft()
                    self.conversationBot.history.appendleft(SYSTEM_PROMPT_MESSAGE)
                    

                await message.channel.send(reply)
                print("Conversation listener normal exit.")
        except Exception as e:
            if DEV:
                print(e)
            print("Conversation listener error.")

        

def setup(bot):
    bot.add_cog(Conversation(bot))
