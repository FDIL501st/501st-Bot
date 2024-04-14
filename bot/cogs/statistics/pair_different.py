from typing import List
import nextcord
from nextcord.ext import commands


from bot.shared.exceptions import FirstAttachmentNotCSVError


class PairDifferent(commands.Cog):
    """Cog for commands related to finding if a pair of data are statistically the same or different."""

    temp_filename: str = "pair_diff.csv"
    temp_file_path: str = "bot/temp/{}".format(temp_filename)

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @staticmethod
    def first_attachment_is_csv(message: nextcord.Message) -> bool:
        """
        Returns if the first attachment of the message is a csv file.
        """
        attachments: List[nextcord.Attachment] = message.attachments

        if len(attachments) == 0:
            # raise FirstAttachmentNotCSVError
            return False
        if attachments[0].content_type != "text/csv; charset=utf-8":
            # raise FirstAttachmentNotCSVError
            return False

        # decided to not use or and combine into the checks into 1 if statement for readability
        return True

    # provide 2 commands, an application message command and a base prefix command
    # both do the same thing

    @nextcord.message_command()
    async def is_pair_statistically_same(self, interaction: nextcord.Interaction, message: nextcord.Message) -> None:
        """
        Given a message that has a csv file, and the csv file has 2 columns,
        returns if both columns of data are statistically the same.
        """

        # check if have csv file as first attachment
        if not PairDifferent.first_attachment_is_csv(message):
            # await interaction.send("First attachment of message used for command wasn't a csv with utf-8 charset.")
            raise FirstAttachmentNotCSVError
            # return

        # await interaction.send("First file of message is a csv file.")

        # now need to save file locally so can use it
        await message.attachments[0].save(PairDifferent.temp_file_path)

        # for now as a placeholder, send the csv file we just saved
        await interaction.send("Saved file",
                               file=nextcord.File(PairDifferent.temp_file_path))

    # @commands.Cog.listener()
    # async def on_application_command_error(self, interaction: nextcord.Interaction, error: nextcord.ApplicationError):
    #     print("Caught error in cog listener")
    #
    #     print("error type is {}".format(type(error)))
    #     print(error)

    # application command error from this cog will call this and the event in __main__.py


def setup(bot: commands.Bot):
    bot.add_cog(PairDifferent(bot))
