#!/usr/bin/env python
from bs4 import BeautifulSoup
import re

def get_category(html_doc):
    with open(html_doc) as f:
        data = f.read()
    soup = BeautifulSoup(data)
    #matches = soup.findAll(text=re.compile("Product Information"))
    matches = soup.findAll('div', id="wayfinding-breadcrumbs_feature_div")
    return matches[0].findAll('li')[-1].text.strip(' \n\t')

if __name__ == "__main__":
    matches = parse('data/B000I97H68')
    print matches