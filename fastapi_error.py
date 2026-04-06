from fastapi import FastAPI
import sentry_sdk

sentry_sdk.init(
    dsn="https://01c834b6d115c65218e3e606af53da5f@o4511170451472384.ingest.de.sentry.io/4511170453962832",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/error/key")
def trigger_key_error():
    """KeyError — required key missing from payment payload."""
    def process_payment(payload):
        return f"Charging ${payload['amount']} to card {payload.get('card_last4', 'xxxx')}"

    process_payment({"card_last4": "4242"})


@app.get("/error/type")
def trigger_type_error():
    """TypeError — string price mixed into arithmetic."""
    def calculate_order_total(items):
        return sum(item["price"] * item["qty"] for item in items)

    calculate_order_total([
        {"name": "Widget", "price": "9.99", "qty": 2},
        {"name": "Gadget", "price": 14.99, "qty": 1},
    ])


@app.get("/error/index")
def trigger_index_error():
    """IndexError — page offset beyond list bounds."""
    def get_page(results, page, page_size=10):
        start = page * page_size
        return results[start]

    get_page(list(range(5)), page=3)


@app.get("/error/value")
def trigger_value_error():
    """ValueError — non-numeric string passed to int()."""
    def create_user(form_data):
        age = int(form_data["age"])
        return {"name": form_data["name"], "age": age}

    create_user({"name": "Charlie", "age": "twenty-five"})


@app.get("/error/zero-division")
def trigger_zero_division_error():
    """ZeroDivisionError — discount calculation with zero item count."""
    def average_item_price(order):
        return order["total"] / order["item_count"]

    average_item_price({"total": 49.99, "item_count": 0})


@app.get("/error/import")
def trigger_import_error():
    """ImportError — optional dependency assumed to be installed."""
    def export_to_excel(data):
        raise ImportError("openpyxl is required but not installed")

    export_to_excel(["col1", "col2"])


@app.get("/error/runtime")
def trigger_runtime_error():
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