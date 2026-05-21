import os
import sys
import threading
import time
import unittest

from test import support


if not support.Py_GIL_DISABLED:
    raise unittest.SkipTest("GIL enabled")


# CI debugging: log each test method to a side file so the workflow's
# resource sampler can `tail -f` it into the live step log. Necessary
# because regrtest's --fast-ci discards the worker's stdout (including
# the verbose unittest output) on a successful test, both inside the
# worker (StringIO capture) and in the parent (show_stdout gating).
_DEBUG_LOG = os.environ.get('CPYTHON_FT_VERBOSE_LOG')
if _DEBUG_LOG:
    _debug_fp = open(_DEBUG_LOG, 'a', buffering=1, encoding='utf-8')
    _debug_lock = threading.Lock()

    def _ft_log(event, test):
        try:
            test_id = test.id()
        except Exception:
            test_id = repr(test)
        ts = time.strftime('%H:%M:%S')
        with _debug_lock:
            _debug_fp.write(f'{ts} {event} {test_id}\n')

    from test.libregrtest import testresult as _ft_testresult
    _ft_R = _ft_testresult.RegressionTestResult
    _ft_orig_start   = _ft_R.startTest
    _ft_orig_success = _ft_R.addSuccess
    _ft_orig_error   = _ft_R.addError
    _ft_orig_failure = _ft_R.addFailure
    _ft_orig_skip    = _ft_R.addSkip

    def _ft_startTest(self, test):
        _ft_log('RUN ', test)
        return _ft_orig_start(self, test)
    def _ft_addSuccess(self, test):
        _ft_log('PASS', test)
        return _ft_orig_success(self, test)
    def _ft_addError(self, test, err):
        _ft_log('ERR ', test)
        return _ft_orig_error(self, test, err)
    def _ft_addFailure(self, test, err):
        _ft_log('FAIL', test)
        return _ft_orig_failure(self, test, err)
    def _ft_addSkip(self, test, reason):
        _ft_log('SKIP', test)
        return _ft_orig_skip(self, test, reason)

    _ft_R.startTest  = _ft_startTest
    _ft_R.addSuccess = _ft_addSuccess
    _ft_R.addError   = _ft_addError
    _ft_R.addFailure = _ft_addFailure
    _ft_R.addSkip    = _ft_addSkip


def load_tests(*args):
    return support.load_package_tests(os.path.dirname(__file__), *args)
