import threading
import gpt4all
import nextcord
from nextcord.ext import commands
from bot.shared.constants import CLUB_SERVER_ID, BOT_ID, CLUB_SERVER_BOT_CHANNEL
from bot.shared.model import gpt_model



CONVERSATION_SYSTEM_PROMPT = """
You are a friend that replies to whatever is said to you. 
"""

class ConversationBot:
    def __init__(self, model: gpt4all.GPT4All) -> None:
        self.model = model
        self._lock = threading.Lock()

    async def reply(self, message: str) -> str:
        """
        Generates a reply to the message, using a gpt4all model.
        If already busy generating, ignore the request by sending a RuntimeError.
        Will not queue for the model.
        """

        if self._lock.acquire(blocking=False):
            try:
                with gpt_model.chat_session(system_prompt=CONVERSATION_SYSTEM_PROMPT):
                    reply = gpt_model.generate(prompt=message, max_tokens=100)  
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
        self.conversationBot: ConversationBot = ConversationBot(gpt_model)


    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        try:
            await self.handle_listener(message)
        except:
            pass

    async def handle_listener(self, message: nextcord.Message):
        # Any message sent to just you(hidden messages) don't have a guild association
        # aka emphemeral message
        if message.guild is None:
            return # do nothing as was unable to find guild from message
        
        # can remove this if later if wanted, for now only occur within club server
        # also only for messages not by the bot (don't want bot endlessly talking to itself)
        # and for now only in the club server bot channel
        if message.guild.id == CLUB_SERVER_ID and message.author.id != BOT_ID and message.channel.id == CLUB_SERVER_BOT_CHANNEL:            
            # for now need to use model to reply to message

            # note: message.reply is a shortcut to ctx.send, what it does is get the context of the message (include channel)
            # and call send to it

            # debug messasge, check wat application id is
            await message.reply(f"{self.bot.application_id=}")
            reply = await self.conversationBot.reply(message.content)
            await message.reply(reply)






def setup(bot):
    bot.add_cog(Conversation(bot))