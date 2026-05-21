import os
import sys
import unittest

from test import support


if not support.Py_GIL_DISABLED:
    raise unittest.SkipTest("GIL enabled")

# CI debugging: force verbose output for this package's worker.
# --fast-ci enables output_on_failure, which (a) sets support.verbose=True
# and (b) redirects sys.stdout/sys.stderr to a StringIO that is discarded
# when the test passes. To make verbose output visible even on success,
# bypass the StringIO by restoring stdout/stderr to the worker's real
# file descriptors (preserved by Python in sys.__stdout__/__stderr__).
# Scoped to this worker subprocess; does not leak to other tests.
support.verbose = True
if sys.__stdout__ is not None:
    sys.stdout = sys.__stdout__
if sys.__stderr__ is not None:
    sys.stderr = sys.__stderr__

def load_tests(*args):
    return support.load_package_tests(os.path.dirname(__file__), *args)
