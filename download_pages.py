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

file_path = '/home/luv/Downloads/ProductId_CellPhone-and-Accessories.txt'

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
        print "downloaded "+pid
    else:
        print "File exists %s" % (pid)
    with open('data/%s' % (pid)) as f:
        html = f.read()
    return html


def process_product_pages(file_path):
    pids = get_product_ids(file_path)
    count = 0
    for pid in pids:
        html = get_product_html(pid)
        out = re.findall(r'Technical Details', html)
        if len(out) > 0:
            count += 1
            print "Kam ke products found till now = " + str(count)



process_product_pages(file_path)
