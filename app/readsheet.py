import re
import sys
import time
import os.path
from pymongo import MongoClient, errors
from apprise import Apprise, AppriseConfig
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = os.getenv('SHEET_ID')
ITEM_CATEGORIES = os.getenv('ITEM_CATEGORIES').split(',')
ITEM_RANGES = os.getenv('ITEM_RANGES').split(',')
SHEET_TAB = 'Sheet1'

ITEMS = dict()
for count, item in enumerate(ITEM_CATEGORIES):
    ITEMS[item] = '%s!%s' % (SHEET_TAB, ITEM_RANGES[count])

API_KEY = os.getenv('SHEETS_API_KEY')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '3600'))

APPRISE_CONFIG_STRING = os.getenv('APPRISE_CONFIG_STRING', None)
APPRISE_CONFIG_URL = os.getenv('APPRISE_CONFIG_URL', None)

update_list = []


def main():
    service = build('sheets', 'v4', developerKey=API_KEY)

    while True:
        print('Checking sheet for updated pricing...')
        # Call the Sheets API
        sheet = service.spreadsheets()  # pylint: disable=no-member

        # Get prices for each category we're interested in
        for key in ITEMS:
            get_prices(sheet, ITEMS[key], key)
        check_prices()
        print('Sleeping for %s seconds before checking again' % CHECK_INTERVAL)
        update_list.clear()
        time.sleep(CHECK_INTERVAL)


def insert_part(part, part_type):
    try:
        client = MongoClient(
            "mongodb://%s/" % DB_HOST, serverSelectionTimeoutMS=10000)
        client.server_info()
    except errors.ServerSelectionTimeoutError:
        print("Failed to connect to the database")
        sys.exit(1)
    db = client.parts   # pylint: disable=invalid-name
    collection = db[part_type]
    # check if part already exists and update the price if necessary
    orig = collection.find_one_and_update(
        {'name': part['name']}, {'$set': {'price': int(part['price'])}})
    # if it doesn't exist add it
    if orig is None:
        collection.insert_one(part)
        print("Found new %s: %s, adding it to the database" %
              (part_type, part['name']))
        body, title = new_item_notif(part)
        send_notification(body, title)
    else:
        # if the price has dropped, add it to a list (we don't care about price increases)
        if orig['price'] > part['price']:
            update_list.append({
                "type": part['type'],
                "name": part['name'],
                "last_price": int(orig['price']),
                "current_price": int(part['price'])
            })
    client.close()


def check_prices():
    if len(update_list) <= 0:
        print('No prices changed since last check')
    else:
        for parts in update_list:
            if parts['current_price'] < parts['last_price']:
                print('%s price dropped $%s' %
                      (parts['name'], (parts['last_price'] - parts['current_price'])))
                body, title = price_drop_notif(parts)
                send_notification(body, title)


def price_drop_notif(part):
    print('Setting price drop notification body')
    price_change = part['last_price'] - part['current_price']
    body = """
<b><h2>Price Drop Alert</h2></b><br>
<p>%s: %s dropped <b>$%d</b>, new price: $%d""" % (
        part['type'], part['name'], price_change, part['current_price'])
    title = 'PC Part Price Drop'
    return body, title


def new_item_notif(part):
    body = """
<b><h2>New Part Alert</h2></b><br>
<p>%s: %s added to database, Price: $%d""" % (
        part['type'], part['name'], part['price'])
    title = 'PC Part Added'
    return body, title


def send_notification(message, subject):
    apprise_client = Apprise()
    if APPRISE_CONFIG_STRING:
        apprise_client.add(APPRISE_CONFIG_STRING)
    if APPRISE_CONFIG_URL:
        config = AppriseConfig()
        config.add(APPRISE_CONFIG_URL)
        apprise_client.add(config)

    res = apprise_client.notify(body=message, title=subject)
    print(res)
    if not res:
        print('Failed to send notification')
    else:
        print('Successfully sent notification')

    return res


def get_prices(sheet, sheet_range, name):
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
            # If it's a row with item name and price process it
            if len(row) > 1:
                try:
                    part['price'] = int(row[1])
                # if price is a range just use the max price
                except ValueError:
                    pattern = re.compile(r'\d+\D+(\d+)')
                    match = pattern.match(row[1])
                    part['price'] = int(match.group(1))

                insert_part(part, name)


if __name__ == '__main__':
    main()
