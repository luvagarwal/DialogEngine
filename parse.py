#!/usr/bin/env python
from bs4 import BeautifulSoup
import re

def parse(html_doc):
    with open(html_doc) as f:
        data = f.read()
    soup = BeautifulSoup(data)
    matches = soup.findAll(text=re.compile("Product Information"))
    for e in matches:
        print e.parent.next_sibling

parse('data/product')
