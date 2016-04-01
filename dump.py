#!/usr/bin/env python
from collections import defaultdict
import MySQLdb

import parse
import download_pages

def run_query(query):
    db = MySQLdb.connect(user="root", passwd="123123", db="dialogengine")
    cur = db.cursor()
    cur.execute(query)

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
        run_create_table_query(features, category)
        run_insert_query(all_info, category, features)
                

def run_create_table_query(features, category):
    " generate an create mysql query "
    query = "create table `%s` (" % (category)
    for f in features:
        query += "`%s`" % (f)
        query += " VARCHAR(50),"
    query = query[:-1]
    query += ");"
    run_query(query)

def run_insert_query(products, category, features):
    " generate an insert mysql query "
    for product in products:
        query = "insert into `%s` " % (category)
        # for f in features:
        #     query += "'%s'," % (f)
        # query = query[:-1]
        # query += ") values ("
        query += " values ("
        flag = 0
        for feature in features:
            flag = 1
            try:
                query += " '%s'," % (product[feature])
            except:
                query += " NULL,"
        query = query[:-1]
        query += ");"
        if flag == 1:
            print query
            run_query(query)

dump()