#!/usr/bin/env python
"""
Downloads the product pages and checks if the term
'Technical Details' exists in it or not.

Change the variable `file_path` to the file of product ids Soureesh gave 
"""

import os
import subprocess
import urllib2
import re
from collections import defaultdict

import parse

file_path = 'ProductId_Electronics.txt'

def get_product_ids(file_path):
    with open(file_path) as f:
        pids = set(f.readlines())
        l = []
        for pid in pids:
            l.append(pid.strip(' \n\t'))
        return l

def get_product_html(pid):
    # proxy_support = urllib2.ProxyHandler({"https":"https://proxy.iiit.ac.in:8080"})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)
    # return urllib2.urlopen(link).read()
    if not os.path.isfile('data/%s' % (pid)):
        FNULL = open(os.devnull, 'w')
        subprocess.Popen(['wget', 'https://amazon.com/dp/%s'%(pid),  '-O', 'data/%s'%(pid)],
                        stdout=FNULL, stderr=subprocess.STDOUT).wait()
    #     print "downloaded "+pid
    # else:
    #     print "File exists %s" % (pid)
    with open('data/%s' % (pid)) as f:
        html = f.read()
    return html

def process_product_pages(file_path):
    pids = get_product_ids(file_path)
    count = 0
    pids_category_wise_num = defaultdict(int)
    pids_category_wise_list = defaultdict(list)
    pids_imp = []
    for pid in pids:
        html = get_product_html(pid)
        out = re.findall(r'Technical Details', html)
        if len(out) > 0:
            try:
                category = parse.get_category('data/%s' % (pid))
            except:
                category = None
            if not category:
                continue
            count += 1
            pids_category_wise_num[category] += 1
            pids_category_wise_list[category].append(pid)
            #os.system('google-chrome https://amazon.com/dp/%s'%(pid))
            print count
            if count % 59 == 0:
                  #print "Kam ke products found till now = " + str(count)
                  break
            #      print pid
            #      print len(pids_category_wise_num)
            #      l = sorted(pids_category_wise_num.items(), key=lambda x: x[1])[-10:]
            #      print l            
    return pids_category_wise_list

if __name__ == '__main__':
    process_product_pages(file_path)
