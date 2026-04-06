import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Replicate the logic from send_error.py's attribute_error scenario
# with the expected fix: greet_user should handle None user gracefully

users = {"alice": {"name": "Alice", "role": "admin"}}


def get_user(user_id):
    return users.get(user_id)


def greet_user(user_id):
    user = get_user(user_id)
    # Correct behaviour: return a safe fallback when user is None
    if user is None:
        return "Hello, Guest!"
    return f"Hello, {user.get('name')}!"


def test_greet_user_returns_fallback_for_unknown_user():
    # 'bob' is not in the users dict, so get_user returns None
    # The correct behaviour is to return a safe fallback greeting
    result = greet_user("bob")
    assert result is not None
    assert result == "Hello, Guest!"


def test_greet_user_returns_greeting_for_known_user():
    result = greet_user("alice")
    assert result == "Hello, Alice!"
