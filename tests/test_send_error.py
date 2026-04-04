import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Patch rollbar.init and rollbar.report_exc_info to avoid real network calls
import unittest.mock as mock
with mock.patch('rollbar.init'), mock.patch('rollbar.report_exc_info'):
    import importlib
    import send_error
    importlib.reload(send_error)

from send_error import greet_user

def test_greet_user_returns_fallback_for_unknown_user():
    result = greet_user("bob")
    # When user is not found, should return a safe fallback greeting rather than crashing
    assert result is not None
    assert isinstance(result, str)
    # Should gracefully handle missing user, e.g. return "Hello, Unknown!" or similar
    assert "Hello" in result
