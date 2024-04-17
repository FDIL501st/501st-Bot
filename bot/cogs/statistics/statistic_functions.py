from typing import Dict
import pandas as pd
import scipy.stats as stats
from bot.shared.errors import IncorrectCSVFormatError


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
    distance_diff_mean_to_bounds: float = score95*diff_std
    if distance_diff_mean_to_zero > distance_diff_mean_to_bounds:
        # check if 0 is out of bounds of confidence interval
        return False

    # assume statistically same even for case where 0 is one of the bounds
    return True
