import nextcord
from nextcord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @nextcord.slash_command()
    async def ping(self, interaction: nextcord.Interaction):
        """Returns ping to bot."""
        ping = round(1000 * self.bot.latency)
        if ping < 200:
            await interaction.send(f"Bot ping is : {ping} ms.")
        else:
            await interaction.send(f"Bot is currently facing some pain. Its ping is : {ping} ms.")

    @nextcord.user_command()
    async def hello(self, interaction: nextcord.Interaction, member: nextcord.Member):
        """From nextcord docs
        Says hi to a user that was right-clicked on"""
        await interaction.response.send_message(f"Hello {member}!")

    @nextcord.message_command()
    async def say(self, interaction: nextcord.Interaction, message: nextcord.Message):
        """From nextcord docs
        Sends the content of the right-clicked message as an ephemeral response"""
        await interaction.response.send_message(message.content, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))
