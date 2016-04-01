#!/usr/bin/env python
import MySQLdb

import parse
import download_pages

def get_cursor():
    db = MySQLdb.connect(user="root", passwd="123123", db="dialogengine")
    return db.cursor()

def dump():
    file_path = 'ProductId_Electronics.txt'
    cur = get_cursor()
    categorized_pids = download_pages.process_product_pages(file_path)
    for category in categorized_pids:
        for pid in categorized_pids[category]:
            info = parse.get_table_info('data/%s'%(pid))
            print info
            break
        # cur.execute()
    