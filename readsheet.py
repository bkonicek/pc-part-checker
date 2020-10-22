import os.path
import pymongo
import re
import time
import apprise
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

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 3600))

APPRISE_CONFIG_STRING = os.getenv('APPRISE_CONFIG_STRING', None)
APPRISE_CONFIG_URL = os.getenv('APPRISE_CONFIG_URL', None)

update_list = []


def main():
    service = build('sheets', 'v4', developerKey=API_KEY)

    while True:
        print('Checking sheet for updated pricing...')
        # Call the Sheets API
        sheet = service.spreadsheets()

        # Get prices for each category we're interested in
        for key in ITEMS.keys():
            getPrices(sheet, ITEMS[key], key)
        check_prices()
        print('Sleeping for %s seconds before checking again' % CHECK_INTERVAL)
        time.sleep(CHECK_INTERVAL)


def insertPart(part, part_type):
    client = pymongo.MongoClient(
        "mongodb://%s/" % DB_HOST)
    db = client.parts
    collection = db[part_type]
    # check if part already exists and update the price if necessary
    orig = collection.find_one_and_update(
        {'name': part['name']}, {'$set': {'price': int(part['price'])}})
    # if it doesn't exist add it
    if orig is None:
        collection.insert_one(part)
        print("Inserted %s: %d" % (part_type, part['name']))
    else:
        # if the price has changed, add it to a list
        if orig['price'] != part['price']:
            update_list.append({
                "type": part['type'],
                "name": part['name'],
                "last_price": int(orig['price']),
                "current_price": int(part['price'])
            })


def check_prices():
    apprise_client = apprise.Apprise()
    if APPRISE_CONFIG_STRING:
        apprise_client.add(APPRISE_CONFIG_STRING)
    if APPRISE_CONFIG_URL:
        apprise_client.add(APPRISE_CONFIG_URL)
    if len(update_list) <= 0:
        print('No prices changed since last check')
    else:
        for parts in update_list:
            if parts['current_price'] < parts['last_price']:
                apprise_client.notify(
                    body='<b><h2>Price Drop Alert</h2></b><br><p>%s: %s dropped <b>$%d</b>, new price: $%d' % (
                        parts['type'], parts['name'], (parts['last_price'] - parts['current_price']), parts['current_price']),
                    title='Fanatech Price Drop'
                )
                # print('%s price dropped $%s' %
                #       (parts['name'], (parts['last_price'] - parts['current_price'])))


def getPrices(sheet, sheet_range, name):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=sheet_range).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            part = {
                "type": name,
                "name": row[0]
            }
            try:
                part['price'] = int(row[1])
            # if price is a range just use the max price
            except:
                p = re.compile(r'\d+\D+(\d+)')
                m = p.match(row[1])
                part['price'] = int(m.group(1))

            insertPart(part, name)


if __name__ == '__main__':
    main()
