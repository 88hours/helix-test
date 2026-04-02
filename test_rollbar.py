import os
import rollbar
from rollbar.logger import RollbarHandler

import logging

rollbar.init(
    access_token=os.getenv('ROLLBAR_ACCESS_TOKEN', 'eced949177b945eeb874994ba338b5ab'),
    environment=os.getenv('ROLLBAR_ENVIRONMENT', 'development'),
    scrub_fields=[
        'password',
        'secret',
        'token',
        'api_key',
        'access_token',
        'authorization',
        'cookie',
        'csrf_token',
    ],
)

rollbar.report_message('Rollbar is configured correctly', 'info')
def payload_handler(payload, **kw):
    # Add person (user) information
    # 'id' is required; email and username are optional
    payload['data']['person'] = {
        'id': '1234',
        'username': 'john.doe',
        'email': 'john@example.com',
    }

    # Add custom metadata for debugging
    payload['data']['custom'] = {
        'trace_id': 'abc123',
        'feature_flags': ['new_ui', 'beta_feature'],
        'user_tier': 'premium',
    }

    return payload

rollbar.events.add_payload_handler(payload_handler)

logger = logging.getLogger(__name__)
logger.addHandler(RollbarHandler())
logger.setLevel(logging.ERROR)

# Now logger.error() will send to Rollbar
logger.error('Something went wrong')
try:
    a = None
    a.hello() # type: ignore
except Exception:
    logger.error('SEND TO ROLLBAR')
    rollbar.report_exc_info()
