import os.path
import pickle

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from core.constants.global_constants import TOKEN_PATH, CREDENTIALS_PATH, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def read_input_data():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values')
    df = pd.DataFrame(values[1:], columns=values[0])
    df = df.loc[(df['Active'] == 'YES')]

    if not values:
        print('No data found.')
        df = ''
        return df
    else:
        return df
