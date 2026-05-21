import os
import unittest

from test import support


if not support.Py_GIL_DISABLED:
    raise unittest.SkipTest("GIL enabled")

# CI debugging: force verbose output for this package's worker.
# Each regrtest worker is a fresh subprocess, so this flag is scoped to
# the worker running test_free_threading and does not leak to other tests.
support.verbose = True

def load_tests(*args):
    return support.load_package_tests(os.path.dirname(__file__), *args)
