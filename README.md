# helix-test

Sample application used to trigger real errors for [Helix](../helix) pipeline testing.

`send_error.py` sends errors to Rollbar, which fires a webhook to the Helix crash handler and kicks off the full agent pipeline.

---

## Setup

**1. Install dependencies**

```bash
pip install rollbar
```

**2. Configure your Rollbar access token**

Open `send_error.py` and replace the `access_token` value with your Rollbar project token:

```python
rollbar.init(
    access_token="your_rollbar_project_token",
    environment="production",
)
```

You can find the token in your Rollbar project under **Settings → Project Access Tokens**.

**3. Make sure Helix is running**

The Helix crash handler must be reachable and your Rollbar webhook must be pointed at it:

```
https://<your-helix-url>/webhook/rollbar
```

Configure this in Rollbar under **Settings → Notifications → Webhook**.

---

## Sending errors

**Send all 8 errors at once:**

```bash
python send_error.py
```

**Send a specific error:**

```bash
python send_error.py attribute_error
```

**Send multiple specific errors:**

```bash
python send_error.py key_error type_error zero_division
```

---

## Available errors

| Name | Error type | Scenario |
|---|---|---|
| `attribute_error` | `AttributeError` | `NoneType` returned from a failed dict lookup |
| `key_error` | `KeyError` | Required key missing from payment payload |
| `type_error` | `TypeError` | String price mixed into arithmetic |
| `index_error` | `IndexError` | Page offset beyond list bounds |
| `value_error` | `ValueError` | Non-numeric string passed to `int()` |
| `zero_division` | `ZeroDivisionError` | Divide by zero in discount calculation |
| `import_error` | `ImportError` | Missing optional dependency |
| `runtime_error` | `RuntimeError` | Database connection pool exhausted |

---

## Demo mode

If you want to test the Helix pipeline without real Rollbar credentials, enable demo mode in Helix so the webhook skips token verification:

```yaml
# helix/config.yaml
demo: true
```

Or via environment variable:

```bash
HELIX_DEMO=true
```

Then POST a payload directly to the crash handler:

```bash
curl -X POST https://<your-helix-url>/webhook/rollbar \
  -H "Content-Type: application/json" \
  -d @../helix/test_payloads/rollbar_new_item.json
```
