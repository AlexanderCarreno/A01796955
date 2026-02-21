"""Run unit tests for the project (placed in tests/).

Usage: `python -m tests.run_tests` or `python tests/run_tests.py` from project root.
"""

import unittest
import sys
import os


def main():
    loader = unittest.TestLoader()
    # Discover tests in this tests/ directory
    tests_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir=tests_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors

    print("\n" + "=" * 70)
    print(f"SUMMARY: {passed} passed, {failures} failures, {errors} errors")
    print(f"Total Tests: {total_tests}")
    print("=" * 70)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
