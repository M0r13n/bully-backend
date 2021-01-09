import json
import logging

import requests

from app.config import WEBHOOK_URL

logger = logging.getLogger(__name__)


def post_message(payload: str):
    response: requests.Response = requests.post(
        WEBHOOK_URL,
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned a {response.status_code} Status-Code: {response.text}")


def send_notification(notification: str) -> bool:
    try:
        payload: str = json.dumps({'text': notification})
        post_message(payload)
        return True
    except Exception as e:
        logger.error(e)
        return False
