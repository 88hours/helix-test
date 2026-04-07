import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the function directly by extracting it from the module
# We need to define/import average_item_price as it's defined inline in the endpoint
# We'll test it via a direct reimplementation match and patch approach

import importlib
import types

def get_average_item_price():
    """Extract the average_item_price function from fastapi_error module context."""
    # Define it as it should behave correctly
    # We'll test the actual function by importing the module and calling the logic
    import fastapi_error
    import inspect
    source = inspect.getsource(fastapi_error.trigger_zero_division_error)
    # We'll just call the inner function logic directly
    # by reconstructing it from the module
    return None


def average_item_price(order):
    """Reference to the actual function under test - copied from source."""
    # This mirrors what the buggy code does; the fix should handle item_count == 0
    if order["item_count"] == 0:
        return 0.0
    return order["total"] / order["item_count"]


def test_average_item_price_returns_zero_when_item_count_is_zero():
    """average_item_price should return 0.0 (or a safe fallback) when item_count is 0."""
    # Import from the actual module by executing the inner function
    import fastapi_error
    import inspect
    import types

    # Get source of trigger_zero_division_error and extract average_item_price
    # Execute the inner function definition
    source = inspect.getsource(fastapi_error.trigger_zero_division_error)
    
    # Build a namespace and exec the inner function
    namespace = {}
    # Extract only the inner function definition lines
    lines = source.split('\n')
    inner_lines = []
    capturing = False
    for line in lines:
        if 'def average_item_price' in line:
            capturing = True
        if capturing:
            # Remove leading indentation (function is indented inside the route)
            inner_lines.append(line[4:] if line.startswith('    ') else line)
            # Stop after the return statement
            if capturing and inner_lines and len(inner_lines) > 1 and inner_lines[-1].strip().startswith('return'):
                break
    
    inner_source = '\n'.join(inner_lines)
    exec(inner_source, namespace)
    actual_average_item_price = namespace['average_item_price']
    
    # The correct behaviour: when item_count is 0, should return 0.0 not raise ZeroDivisionError
    result = actual_average_item_price({"total": 49.99, "item_count": 0})
    assert result == 0.0, f"Expected 0.0 for zero item_count, got {result}"
