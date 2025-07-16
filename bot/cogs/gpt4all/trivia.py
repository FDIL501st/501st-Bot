import asyncio
import nextcord
from nextcord.ext import commands
from random import choice
from bot.shared.model import gpt_model


prompts: list[str] = [
    "Give me a fact about {topic}.",
    "Give me a cool fact about {topic}",
    "Tell me something interesting about {topic}.",
    "Tell me a funny fact about {topic}.",
    "Tell me something about {topic}.",
    "I want to know something cool about {topic}.",
    "Share me a fascinating fact about {topic}.",
    "Share me a rare fact about {topic}.",
    "Share with me a fact about {topic}."

]

TRIVIA_SYSTEM_PROMPT = """
You are a trivia fact generator. Your task is to provide a fact about a topic.
Make sure your facts are accurate, engaging, and relevant to the topic. 
Avoid repeating the same fact and try to provide a variety of information. 
Also try to keep your responses short.
"""

class Trivia(commands.Cog):
    """
    The trivia giver commands.
    """
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @nextcord.slash_command()
    async def fact(self, interaction: nextcord.Interaction, topic: str):
        """
        Generates a fact on a topic. Facts are generated with AI, so they may not be accurate.

        Parameters
        ----------
        interaction
            The interaction object
        topic
            The topic to generate a fact about. This is a required argument.
        """
        # defer response so we got time for AI to generate resopnse
        # (default tiemout is 3s)
        # defer gives 15 min to respond

        await interaction.response.defer()
        fact = await self.generate_fact(topic=topic)
        await interaction.followup.send(content=fact)


    @commands.command(alias=["fact"])
    async def ai_fact(self, ctx: commands.Context, *topic):
        """Generates a fact on a topic. Facts are generated with AI, so they may not be accurate.

        Args:
            ctx (commands.Context): command context. This is not provided by the user
            topic (tuple[str]): The topic to generate a fact about. This is a required argument.
        """
        async with ctx.typing():
            fact_coroutine = asyncio.create_task(self.generate_fact(topic=" ".join(topic)))
            # add a 60s sleep to force typing to keep happening
            # average time it takes for generate_fact to complete
            # for some reason, generate_fact doesn't keep typing for the entire time, so manually do it with sleep
            
            await asyncio.sleep(60) # doesn't seem to work anymore?
            
            fact = await fact_coroutine

            # other context managers or waits (like event.wait, or await) don't keep typing active
            # things like thread joins also don't work
            # sleep works, or a loop

        await ctx.send(fact)

    async def generate_fact(self, topic: str) -> str:
        """
        Generates a fact about a topic, using a gpt4all model.
        """
        prompt: str = choice(prompts).format(topic=topic)
        with gpt_model.chat_session(system_prompt=TRIVIA_SYSTEM_PROMPT):
            fact = gpt_model.generate(prompt=prompt)
        return fact
    
    # need to define an error handling function for ai_fact 
    # In on_command_error, caught exception of type: <class 'nextcord.ext.commands.errors.MissingRequiredArgument'>



def setup(bot: commands.Bot):
    bot.add_cog(Trivia(bot))


