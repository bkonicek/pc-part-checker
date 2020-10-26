import os
from pymongo import MongoClient

DB_HOST = os.getenv('DB_HOST', 'localhost:27017')


def main():
    client = MongoClient('mongodb://%s' % DB_HOST)
    db = client.parts
    collection = db[db.list_collection_names()[0]]
    part = collection.find_one()
    collection.update_one({'name': part['name']}, {
                          '$set': {'price': part['price'] + 10}})
    print('Updated %s\'s price from %s to %s' %
          (part['name'], part['price'], (part['price'] + 10)))
    client.close()


if __name__ == '__main__':
    main()
