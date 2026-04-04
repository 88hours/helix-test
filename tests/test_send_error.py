import pytest
from send_error import greet_user


def test_greet_user_with_nonexistent_user_raises_attribute_error():
    """Test that greet_user raises AttributeError when user_id doesn't exist."""
    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'get'"):
        greet_user("bob")
