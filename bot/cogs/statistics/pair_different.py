from typing import List, Dict
import nextcord
from nextcord.ext import commands
import pandas as pd
import scipy.stats as stats
from bot.shared.errors import FirstAttachmentNotCSVError
from bot.shared.errors import IncorrectCSVFormatError


class PairDifferent(commands.Cog):
    """Cog for commands related to finding if a pair of data are statistically the same or different."""

    temp_filename: str = "pair_diff.csv"
    temp_file_path: str = "tmp/{}".format(temp_filename)

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
        Given a message that has a csv file, and the csv file has a reader row and 2 columns,
        returns if both columns of data are statistically the same using a 95% confidence interval.
        At the moment the algorithm for this command needs fixing.
        """

        # check if have csv file as first attachment
        if not PairDifferent.first_attachment_is_csv(message):
            # await interaction.send("First attachment of message used for command wasn't a csv with utf-8 charset.")
            raise FirstAttachmentNotCSVError
            # return

        # await interaction.send("First file of message is a csv file.")

        # now need to save file locally so can use it
        await message.attachments[0].save(PairDifferent.temp_file_path)

        csv: pd.DataFrame = pd.read_csv(PairDifferent.temp_file_path)

        result: bool = PairDifferent.is_pair_data_statistically_same(csv)
        # overwrite csv and send back to user to see the column added, so they can see what we did
        csv.to_csv(PairDifferent.temp_file_path)
        if result:
            await interaction.send("The paired data are statistically the same.",
                                   file=nextcord.File(PairDifferent.temp_file_path))
            return

        await interaction.send("The paired data are not statistically the same.",
                               file=nextcord.File(PairDifferent.temp_file_path))

    # @commands.Cog.listener()
    # async def on_application_command_error(self, interaction: nextcord.Interaction, error: nextcord.ApplicationError):
    #     print("Caught error in cog listener")
    #
    #     print("error type is {}".format(type(error)))
    #     print(error)

    # application command error from this cog will call this and the event in __main__.py

    @staticmethod
    def is_pair_data_statistically_same(df: pd.DataFrame) -> bool:
        """
        Returns if pair data is statistically the same using 95% confidence interval.
        Expects 2 columns of data.
        """
        # get first row and print its size, this is number of columns
        num_col: int = df.iloc[:1].size
        if num_col != 2:
            raise IncorrectCSVFormatError("Expected csv to have only 2 columns.")

        # need to do a type check for numerical data

        # add a third column which is difference between column 0 and 1
        diff: str = "pair_difference"
        df[diff] = df.iloc[:, 0] - df.iloc[:, 1]

        # get a mean and standard deviation of diff column
        diff_mean: float = df[diff].mean()
        diff_std: float = df[diff].std()  # use sample size correction version, where divide by n-1, not n

        # need to determine if we use student t or z (# of rows <=30)
        num_row: int = df.iloc[:, 0].size

        if num_row > 30:
            # use z-score 95% confidence interval
            score95: float = 1.96

        else:
            # use students to for 95% confidence interval
            score95: float = stats.t.ppf(0.975, num_row)

        # diff_confidence_interval_lower: float = diff_mean - z95 * diff_std
        # diff_confidence_interval_upper: float = diff_mean + z95 * diff_std
        # # now we check if 0 is within lower and upper bounds, inclusive
        # if diff_confidence_interval_lower <= 0 <= diff_confidence_interval_upper:
        #     return True
        #
        # return False

        # other option is to check if the distance of diff_mean to 0 is less than diff_mean to the bounds
        # how it works is that 0 will be within the confidence interval
        # if the distance between diff_mean and 0 is less than distance from diff_mean to the bounds
        # this is one comparison as diff_mean is in center of the confidence interval bounds

        distance_diff_mean_to_zero: float = abs(diff_mean)
        distance_diff_mean_to_bounds: float = score95 * diff_std
        if distance_diff_mean_to_zero > distance_diff_mean_to_bounds:
            # check if 0 is out of bounds of confidence interval
            return False

        # assume statistically same even for case where 0 is one of the bounds
        return True


def setup(bot: commands.Bot):
    bot.add_cog(PairDifferent(bot))
