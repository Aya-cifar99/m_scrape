import json
import os

with open(f"../core/properties/muvi_properties.json") as json_file:
    properties = json.load(json_file)

# MUVI - SLACK Credentials
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
SLACK_MAIN_CHANNEL_NAME = properties.get('SLACK_MAIN_CHANNEL_NAME')
SLACK_WARNING_CHANNEL_NAME = properties.get('SLACK_WARNING_CHANNEL_NAME')
# MUVI - GOOGLE INPUT SHEET
SAMPLE_SPREADSHEET_ID = properties.get("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = properties.get("SAMPLE_RANGE_NAME")
TOKEN_PATH = f'{os.environ.get("GOOGLESHEET_CREDENTIAL_FILE_PATH")}/token.pickle'
CREDENTIALS_PATH = f'{os.environ.get("GOOGLESHEET_CREDENTIAL_FILE_PATH")}/credentials.json'

# MUVI - AWS
BUCKET_NAME = properties.get('BUCKET_NAME')
REGION = properties.get('REGION')

# MUVI - PROXY CREDENTIALS
PROXY_USERNAME = os.environ.get("PROXY_USERNAME")
PROXY_PASSWORD = os.environ.get("PROXY_PASSWORD")