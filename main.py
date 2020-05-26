import os
import json
import pickle
from flask import Flask
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

app = Flask(__name__)

@app.route('/')
def get():
    return json.dumps(get_sheet()), 200

def get_sheet():
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    spreadsheet_id = os.getenv('SHEET_ID')
    worksheet_id = int(os.getenv('WORKSHEET_ID'))

    creds = pickle.loads(bytearray.fromhex(os.getenv('TOKEN')))

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.get(spreadsheetId=spreadsheet_id).execute()
    for worksheet in result['sheets']:
        if worksheet['properties']['sheetId'] == worksheet_id:
            worksheet_name = worksheet['properties']['title']
    range_name = f'{worksheet_name}!A3:D'
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    return values

if __name__ == "__main__":
    app.run()
