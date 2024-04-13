import nextcord
from nextcord.ext import commands
from bot.shared.constants import CLUB_SERVER_ID
from bot.shared.checks import is_in_club_server


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

    @commands.Cog.listener()
    async def on_message(self, message):
        # the word we are listening for
        word: str = "Zbeub"

        if message.guild.id == CLUB_SERVER_ID and message.content == word:
            channel = message.guild.get_channel(message.channel.id)
            # Don't use bot.get_channel(), won't find the channel
            # message.guild gets guild the message is from, guild has method get_channel()
            await channel.send(
                "I don't know what {0} means, but someone said it in the club server.".format(word)
            )


def setup(bot: commands.Bot):
    bot.add_cog(Basic(bot))
