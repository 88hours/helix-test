import pytest
from send_error import greet_user

def test_greet_user_raises_attribute_error_for_unknown_user():
    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'get'"):
        greet_user("bob")
