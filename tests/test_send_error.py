import pytest
from send_error import greet_user

def test_greet_user_raises_for_unknown_user():
    """greet_user('bob') should not raise AttributeError when the user is not found."""
    # Before the fix, get_user returns None for 'bob', and user.get('name')
    # raises AttributeError: 'NoneType' object has no attribute 'get'.
    # This test reproduces that crash.
    with pytest.raises(AttributeError):
        greet_user("bob")
