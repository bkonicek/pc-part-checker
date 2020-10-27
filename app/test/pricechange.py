import os
import sys
from pymongo import MongoClient

DB_HOST = os.getenv('DB_HOST', 'localhost:27017')


def create_client():
    client = MongoClient('mongodb://%s' % DB_HOST)
    return client


def price_change(client):
    db = client.parts
    collection = db[db.list_collection_names()[0]]
    part = collection.find_one()
    collection.update_one({'name': part['name']}, {
                          '$set': {'price': part['price'] + 10}})
    print('Updated %s\'s price from %s to %s' %
          (part['name'], part['price'], (part['price'] + 10)))


def list_all(client):
    db = client.parts
    collection = db[db.list_collection_names()[0]]
    for part in collection.find():
        print(part)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Invalid number of arguments. Use either `pricechange` or `dump`')
        sys.exit(1)
    client = create_client()
    if sys.argv[1] == 'pricechange' or len(sys.argv) == 1:
        price_change(client)
    elif sys.argv[1] == 'dump':
        list_all(client)
    client.close()
