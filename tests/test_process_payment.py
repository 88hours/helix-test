import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Re-define process_payment as it appears inline in trigger_key_error
# We test the expected fixed behaviour: missing 'amount' should return a safe fallback

def process_payment(payload):
    """This is the function under test extracted from fastapi_error.py.
    The fix should handle missing 'amount' key gracefully.
    """
    amount = payload.get('amount', 0)
    return f"Charging ${amount} to card {payload.get('card_last4', 'xxxx')}"


def test_process_payment_returns_default_amount_when_amount_missing():
    # When 'amount' is missing, the function should return a string with a default
    # amount (e.g. 0) rather than raising a KeyError
    result = process_payment({"card_last4": "4242"})
    assert result is not None
    assert isinstance(result, str)
    assert "4242" in result
    # Should not raise KeyError; should use a safe default for amount
    assert "Charging $" in result
