from send_error import greet_user

def test_greet_user_returns_greeting_for_valid_username():
    result = greet_user("bob")
    assert result is not None
    assert isinstance(result, str)
    assert "bob" in result.lower() or "Hello" in result
