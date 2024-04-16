from typing import Tuple, Dict, TypeAlias
from dataclasses import dataclass
import unittest
from scipy.stats import t


@dataclass
class TestInput:
    expected: float
    p_value: float
    df: int


class TestTPpf(unittest.TestCase):
    """
    Testing t.ppf to see if it provides what I want.
    What I'm looking for the t value given a tail and degrees of freedom.
    """

    test_inputs: Tuple[TestInput] = (
        TestInput(2.228, 0.975, 10),
        TestInput(2.571, 0.975, 5),
        TestInput(4.303, 0.975, 2),
        TestInput(1.962, 0.975, 1000),
        TestInput(3.850, 0.9995, 20)
    )

    def test_t_ppf(self):
        for test_input in TestTPpf.test_inputs:
            with self.subTest(msg="Run with: {}".format(test_input)):
                expected: float = test_input.expected
                actual: float = t.ppf(test_input.p_value, test_input.df)
                actual = round(actual, 3)
                # our expected values only got 3 decimal places, so need to match # of decimals
                self.assertAlmostEqual(expected, actual, delta=0.001)


if __name__ == '__main__':
    unittest.main()
