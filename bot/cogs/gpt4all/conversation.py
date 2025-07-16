import asyncio
import os
import threading
import nextcord
from nextcord.ext import commands
from bot.shared.constants import CLUB_SERVER_ID, BOT_ID, CLUB_SERVER_BOT_CHANNEL
from bot.shared.model import my_gpt_model, MyGPT4All, MessageType
from collections import deque

DEV: bool = bool(os.environ.get("DEV", "False"))

CONVERSATION_SYSTEM_PROMPT = """
You are a friend that replies to whatever is said to you. Your name is bot.
"""

SYSTEM_PROMPT_MESSAGE: MessageType = {"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}

class ConversationBot:
    def __init__(self, model: MyGPT4All) -> None:
        self.model = model
        self.history: deque[MessageType] = deque([SYSTEM_PROMPT_MESSAGE], maxlen=41)
        # first element at all times needs to be SYSTEM_PROMPT_MESSAGE

        # maxlen takes care of automatically removing from other side
        # this gives us a context of last 20 messages with bot
        # need 1 extra space for SYSTEM_PROMPT_MESSAGE

        self._lock = threading.Lock()


    def reply(self, message: str) -> str:
        """
        Generates a reply to the message, using a gpt4all model.
        If already busy generating, ignore the request by sending a RuntimeError.
        Will not queue for the model.
        """

        if self._lock.acquire(blocking=False):
            try:
                with self.model.chat_session(system_prompt=CONVERSATION_SYSTEM_PROMPT):
                    # manually set model history
                    self.model._history = list(self.history)
                    reply = self.model.generate(prompt=message, max_tokens=100)  
                return reply
            finally:
                # finally block runs before return in try
                self._lock.release()
        else:
            raise RuntimeError("Conversation bot not available, currently working on generating another response.")



class Conversation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot: commands.Bot = bot
        self.conversationBot: ConversationBot = ConversationBot(my_gpt_model)


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
                print("Conversation listener enter.")
                print(f"{self.conversationBot.history}")

                # for now need to use model to reply to message
                async with message.channel.typing():
                    reply_coro = asyncio.to_thread(self.conversationBot.reply, message.content)

                    # give bot 30s think time
                    await asyncio.sleep(30)     # don't think this is working to keep typing indicator active for 30s

                    reply = await reply_coro
                
                    # add message and reply to history
                    self.conversationBot.history.append({"role": "user", "content": message.content})
                    self.conversationBot.history.append({"role": "assistant", "content": reply})

                    # add system_prompt to front again (it was removed if our deque reached its max capacity)
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