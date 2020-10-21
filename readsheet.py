from __future__ import print_function
import os.path
import pymongo
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

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')


def main():
    service = build('sheets', 'v4', developerKey=API_KEY)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Get prices for each category we're interested in
    for key in ITEMS.keys():
        getPrices(sheet, ITEMS[key], key)


def insertPart(part, part_type):
    client = pymongo.MongoClient(
        "mongodb://%s/" % DB_HOST)
    db = client.parts
    collection = db[part_type]
    orig = collection.find_one_and_update(
        {'name': part['name']}, {'$set': {'price': part['price']}})
    if orig is None:
        collection.insert_one(part)
        print("Inserted %s: %s" % (part_type, part['name']))

    check_prices()
    # print(db)


def getPrices(sheet, sheet_range, name):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=sheet_range).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        # print('%s, Price:' % name)
        for row in values:
            # print('%s, %s' % (row[0], row[1]))
            part = {
                "type": name,
                "name": row[0],
                "price": row[1]
            }
            # print(part)
            insertPart(part, name)


if __name__ == '__main__':
    main()
