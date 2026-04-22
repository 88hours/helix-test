"""
Sends sample Python errors to Rollbar for Helix pipeline testing.

Usage:
    python send_error.py                  # sends all errors
    python send_error.py attribute_error  # sends one specific error by name

Available error names:
    attribute_error   — AttributeError: NoneType has no attribute 'get'
    key_error         — KeyError: missing dict key in payment processing
    type_error        — TypeError: unsupported operand type in order total
    index_error       — IndexError: list index out of range in pagination
    value_error       — ValueError: invalid literal in user age parsing
    zero_division     — ZeroDivisionError: divide by zero in discount calc
    import_error      — ImportError: missing optional dependency
    runtime_error     — RuntimeError: database connection pool exhausted
"""

import sys

import rollbar

rollbar.init(
    access_token="ec4d0cf25e02495cb57fbac0e5ab23a7",
    environment="production",
)


_user_store = {"alice": {"name": "Alice", "role": "admin"}}


def greet_user(username):
    user = _user_store.get(username)
    if user is None:
        return f"Hello, {username}!"
    return f"Hello, {user.get('name')}!"


# ---------------------------------------------------------------------------
# Error scenarios
# ---------------------------------------------------------------------------

def attribute_error():
    """AttributeError — NoneType returned from a dict lookup."""
    users = {"alice": {"name": "Alice", "role": "admin"}}

    def get_user(user_id):
        return users.get(user_id)

    def greet_user(user_id):
        user = get_user(user_id)
        # bug: user is None for unknown IDs
        return f"Hello, {user.get('name')}!"

    greet_user("bob")


def key_error():
    """KeyError — required key missing from payment payload."""
    def process_payment(payload):
        # bug: 'amount' key may not be present
        return f"Charging ${payload['amount']} to card {payload.get('card_last4', 'xxxx')}"

    process_payment({"card_last4": "4242"})


def type_error():
    """TypeError — string price mixed into arithmetic."""
    def calculate_order_total(items):
        # bug: price stored as string instead of float
        return sum(item["price"] * item["qty"] for item in items)

    calculate_order_total([
        {"name": "Widget", "price": "9.99", "qty": 2},
        {"name": "Gadget", "price": 14.99,  "qty": 1},
    ])


def index_error():
    """IndexError — page offset beyond list bounds."""
    def get_page(results, page, page_size=10):
        # bug: no bounds check before slicing
        start = page * page_size
        return results[start]

    get_page(list(range(5)), page=3)


def value_error():
    """ValueError — non-numeric string passed to int()."""
    def create_user(form_data):
        # bug: age field not validated before conversion
        age = int(form_data["age"])
        return {"name": form_data["name"], "age": age}

    create_user({"name": "Charlie", "age": "twenty-five"})


def zero_division():
    """ZeroDivisionError — discount calculation with zero item count."""
    def average_item_price(order):
        # bug: no guard when item_count is 0
        return order["total"] / order["item_count"]

    average_item_price({"total": 49.99, "item_count": 0})


def import_error():
    """ImportError — optional dependency assumed to be installed."""
    def export_to_excel(data):
        import openpyxl  # bug: not in requirements
        wb = openpyxl.Workbook()
        wb.active.append(data)

    export_to_excel(["col1", "col2"])


def runtime_error():
    """RuntimeError — database connection pool exhausted."""
    def get_db_connection(pool):
        if pool["available"] == 0:
            raise RuntimeError(
                f"Database connection pool exhausted "
                f"(max={pool['max']}, in_use={pool['in_use']})"
            )
        pool["available"] -= 1
        return pool

    get_db_connection({"max": 10, "in_use": 10, "available": 0})


# ---------------------------------------------------------------------------
# Registry and runner
# ---------------------------------------------------------------------------

ERRORS = {
    "attribute_error": attribute_error,
    "key_error":       key_error,
    "type_error":      type_error,
    "index_error":     index_error,
    "value_error":     value_error,
    "zero_division":   zero_division,
    "import_error":    import_error,
    "runtime_error":   runtime_error,
}


def send(name, fn):
    try:
        fn()
    except Exception:
        rollbar.report_exc_info()
        print(f"  ✓ {name} sent to Rollbar")


if __name__ == "__main__":
    targets = sys.argv[1:] or list(ERRORS.keys())

    unknown = [t for t in targets if t not in ERRORS]
    if unknown:
        print(f"Unknown error(s): {', '.join(unknown)}")
        print(f"Available: {', '.join(ERRORS)}")
        sys.exit(1)

    print(f"Sending {len(targets)} error(s) to Rollbar...\n")
    for name in targets:
        send(name, ERRORS[name])
    print("\nDone.")
