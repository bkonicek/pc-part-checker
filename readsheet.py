from __future__ import print_function
import os.path
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = os.getenv('SHEET_ID')
ITEM_CATEGORIES = os.getenv('ITEM_CATEGORIES').split(',')
ITEM_RANGES = os.getenv('ITEM_RANGES').split(',')
SHEET_TAB = 'Sheet1'

ITEMS = dict()
for x in range(len(ITEM_CATEGORIES)):
    ITEMS[ITEM_CATEGORIES[x]] = '%s!%s' % (SHEET_TAB, ITEM_RANGES[x])

API_KEY = os.getenv('SHEETS_API_KEY')


def main():
    service = build('sheets', 'v4', developerKey=API_KEY)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Get prices for each category we're interested in
    for key in ITEMS.keys():
        getPrices(sheet, ITEMS[key], key)


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
