import unittest
from scipy.stats import ttest_rel
from numpy import mean


# noinspection SpellCheckingInspection
class TestTtestRel(unittest.TestCase):
    """Test case for scipy.stats.ttest_rel()"""

    def setUp(self):
        self.a: list = [3, 5, 6, 7]
        self.related_b = [0, -20, 40, -400]

        self.unrelated_b = [-100, -100, -103, -101]

    def test_ttest_rel_related(self):
        results = ttest_rel(self.a, self.related_b)
        # print(results)

        (lo, hi) = results.confidence_interval()
        # want to assert that 0 is in between lo and hi

        self.assertGreaterEqual(0.0, lo)
        self.assertLessEqual(0.0, hi)

    def test_ttest_rel_unrelated(self):
        results = ttest_rel(self.a, self.unrelated_b)
        # print(results)

        (lo, hi) = results.confidence_interval()

        # want to assert 0 is not in between lo and hi

        # 0 < lo or 0 > hi
        # we are not testing both assertions unlike with 0 in between lo and hi

        # what we will do is fail the test if in between lo and hi
        if lo <= 0 <= hi:
            self.fail("Found that 0 is in range [lo, hi], though it shouldn't be for unrelated data.")


if __name__ == '__main__':
    unittest.main()
