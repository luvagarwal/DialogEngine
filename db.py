from collections import defaultdict
from pymongo import MongoClient

import parse
import download_pages


def getDB():
    client = MongoClient()
    db = client.dialogengine
    return db

def getCollections():
    db = getDB()
    return db.collection_names()

def findProductFeatureValue(product, feature):
    db = getDB()
    colls = getCollections()
    for coll in colls:
        cursor = db[coll].find({"Brand Name": product})
        docs = [d for d in cursor]
        if len(docs) == 0:
            continue
        for doc in docs:
            try:
                return doc[feature]
            except:
                pass

def insert_one(table, value):
    db = getDB()
    db[table].insert_one(value)

def insert_many(table, values):
    db = getDB()
    print table
    print values
    db[table].insert_many(values)

def dump():
    file_path = 'ProductId_Electronics.txt'
    categorized_pids = download_pages.process_product_pages(file_path)
    for category in categorized_pids:
        all_info = []
        all_features = []
        for pid in categorized_pids[category]:
            info = parse.get_table_info('data/%s'%(pid))
            if not info:
                continue
            # all_features += info.keys()
            all_info.append(info)
        # features = set(all_features)
        if len(all_info) == 0:
            continue
        insert_many(category, all_info)


if __name__ == "__main__":
    dump()