# runs all test cases

from typing import Any, Sequence
import unittest

# import modules with Test Cases
import tests_scipy.test_ttest_rel as t1
import tests_scipy.test_t_ppf as t2


def init_test_suite(test_modules: Sequence[Any]) -> unittest.TestSuite:
    """Returns a test suite loaded with the test from the modules."""

    # initialize test suite
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    for module in test_modules:
        test_suite.addTests(loader.loadTestsFromModule(module))

    return test_suite


if __name__ == '__main__':
    # create test suite
    modules = (t1, t2)
    suite: unittest.TestSuite = init_test_suite(modules)

    verbosity_level: int = 2

    # initialize and run test runner with test suite
    runner = unittest.TextTestRunner(verbosity=verbosity_level)
    runner.run(suite)

