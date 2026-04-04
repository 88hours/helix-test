"""
Sends a sample Python error to Rollbar.

Run with:
    python send_error.py
"""

import rollbar

rollbar.init(
    access_token="ec4d0cf25e02495cb57fbac0e5ab23a7",
    environment="production",
)


def get_user(user_id):
    users = {"alice": {"name": "Alice", "role": "admin"}}
    # Bug: user_id "bob" is not in the dict — returns None
    return users.get(user_id)


def greet_user(user_id):
    user = get_user(user_id)
    # This will raise AttributeError: 'NoneType' object has no attribute 'get'
    return f"Hello, {user.get('name')}!"


if __name__ == "__main__":
    try:
        greet_user("bob")
    except Exception:
        rollbar.report_exc_info()
        print("Error sent to Rollbar.")
