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

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0