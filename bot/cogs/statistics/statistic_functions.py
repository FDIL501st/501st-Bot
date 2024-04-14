from typing import Dict
import pandas as pd
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

    # need to determine if use t-test or z-test (# of rows <=30)
    num_row: int = df.iloc[:, 0].size

    # use z-score for 95% confidence interval
    z95: float = 1.96

    diff_confidence_interval_lower: float = diff_mean - z95 * diff_std
    diff_confidence_interval_upper: float = diff_mean + z95 * diff_std

    # now we check if 0 is within lower and upper bounds, inclusive
    if diff_confidence_interval_lower <= 0 <= diff_confidence_interval_upper:
        return True

    return False
