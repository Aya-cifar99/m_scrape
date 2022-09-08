import json
import logging

import requests

from core.constants.global_constants import WEBHOOK_URL, SLACK_WARNING_CHANNEL_NAME


def send_slack_message(message, channel=SLACK_WARNING_CHANNEL_NAME):
    payload = {
        "channel": channel,
        "text": message,
        "username": "Muvi Crawler"
    }
    logging.error(message)
    return requests.post(WEBHOOK_URL, data=json.dumps(payload))