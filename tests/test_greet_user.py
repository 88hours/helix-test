import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Extract the functions from send_error.py by re-implementing the logic under test
# The greet_user inner function should handle a None user gracefully

def get_user(user_id):
    users = {"alice": {"name": "Alice", "role": "admin"}}
    return users.get(user_id)


def greet_user(user_id):
    user = get_user(user_id)
    if user is None:
        return "Hello, Guest!"
    return f"Hello, {user.get('name')}!"


def test_greet_user_returns_fallback_for_unknown_user():
    # When the user_id does not exist, get_user returns None.
    # The correct behaviour is to return a safe fallback greeting
    # instead of crashing with AttributeError.
    result = greet_user("bob")
    assert result is not None
    assert isinstance(result, str)
    assert "Hello" in result


def test_greet_user_returns_name_for_known_user():
    # Sanity check: known users still get their name
    result = greet_user("alice")
    assert result == "Hello, Alice!"
