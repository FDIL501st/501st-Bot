import nextcord
from nextcord.ext import commands


class Calculator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @nextcord.slash_command()
    async def calculator(self, interaction: nextcord.Interaction):
        """Calculator"""


def setup(bot: commands.Bot):
    bot.add_cog(Calculator(bot))
