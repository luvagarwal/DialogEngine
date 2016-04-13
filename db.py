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
        cursor = db[coll].find({"brand name": product})
        docs = [d for d in cursor]
        if len(docs) == 0:
            continue
        for doc in docs:
            try:
                return doc[feature]
            except:
                pass
    for coll in colls:
        cursor = db[coll].find({"brand": product})
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

def pushintofile(features, tp):
    if len(features) == 0:
        return
    features = '\n'.join(str(feature) for feature in features)
    features += '\n'
    with open('%sForSpellChecking.txt'%(tp), 'a+') as f:
        f.write(features)

def get_all_brands(all_info):
    all_brands = []
    for info in all_info:
        try:
            brand = info["brand name"]
        except:
            try:
                brand = info["brand"]
            except:
                brand = None
        if brand:
            all_brands.append(brand)
    return all_brands

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
            all_features += info.keys()
            all_info.append(info)
        features = set(all_features)
        pushintofile(features, "features")
        all_brands = get_all_brands(all_info)
        pushintofile(all_brands, "brands")
        if len(all_info) == 0:
            continue
        insert_many(category, all_info)


if __name__ == "__main__":
    dump()