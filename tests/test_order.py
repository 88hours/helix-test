import pytest


def calculate_order_total(items):
    return sum(float(item["price"]) * item["qty"] for item in items)


def test_calculate_order_total_returns_correct_sum_with_string_price():
    items = [
        {"name": "Widget", "price": "9.99", "qty": 2},
        {"name": "Gadget", "price": 14.99, "qty": 1},
    ]
    # The correct total should be 9.99*2 + 14.99*1 = 19.98 + 14.99 = 34.97
    result = calculate_order_total(items)
    assert abs(result - 34.97) < 0.001
