import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch

# Patch rollbar.init and rollbar.report_exc_info to avoid side effects
with patch('rollbar.init'), patch('rollbar.report_exc_info'):
    import importlib
    import send_error
    importlib.reload(send_error)

from send_error import greet_user


def test_greet_user_returns_fallback_for_unknown_user():
    # When 'bob' is not in the users dict, greet_user should return a safe fallback
    # rather than raising an AttributeError.
    result = greet_user('bob')
    # The correct behaviour is to return a greeting with a fallback name (e.g. 'Unknown')
    # or a safe default string instead of crashing.
    assert result is not None
    assert isinstance(result, str)
    assert 'Hello' in result
