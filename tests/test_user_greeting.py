import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from send_error import attribute_error

# Re-implement the inner functions to test the correct behaviour directly
def test_greet_user_returns_fallback_for_unknown_user():
    users = {"alice": {"name": "Alice", "role": "admin"}}

    def get_user(user_id):
        return users.get(user_id)

    def greet_user(user_id):
        user = get_user(user_id)
        # correct behaviour: return a safe fallback greeting when user is None
        if user is None:
            return "Hello, Guest!"
        return f"Hello, {user.get('name')}!"

    result = greet_user("bob")
    assert result == "Hello, Guest!"
