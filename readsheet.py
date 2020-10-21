from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = os.getenv('SHEET_ID')
CPU_RANGE = 'Sheet1!A2:B22'
GPU_RANGE = 'Sheet1!C2:D'
MB_RANGE = 'Sheet1!E2:F'

API_KEY = os.getenv('SHEETS_API_KEY')


def main():
    service = build('sheets', 'v4', developerKey=API_KEY)

    # # Call the Sheets API
    sheet = service.spreadsheets()

    # Get prices for each item category
    getPrices(sheet, CPU_RANGE, 'CPU')
    getPrices(sheet, GPU_RANGE, 'GPU')
    getPrices(sheet, MB_RANGE, 'Motherboard')


def getPrices(sheet, sheet_range, name):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=sheet_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('%s, Price:' % name)
        for row in values:
            print('%s, %s' % (row[0], row[1]))


if __name__ == '__main__':
    main()
