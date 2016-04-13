#!/usr/bin/env python
from bs4 import BeautifulSoup
import re

def make_soup(file_path):
    with open(file_path) as f:
        data = f.read()
    return BeautifulSoup(data)

def get_category(file_path):
    soup = make_soup(file_path)
    #matches = soup.findAll(text=re.compile("Product Information"))
    matches = soup.findAll('div', id="wayfinding-breadcrumbs_feature_div")
    return matches[0].findAll('li')[-1].text.strip(' \n\t')

def get_price(file_path):
    soup = make_soup(file_path)
    try:
        matches = soup.findAll('span', id="priceblock_ourprice")[0]
        price = matches.text.strip(' \n\t')
    except:
        price = 'NULL'
    return price

def get_table_info(file_path):
    soup = make_soup(file_path)

    # TO-CORRECT
    data = soup.findAll('h1', text=re.compile("Technical Details"))
    try:
        data = data[0].parent
    except:
        return None
    table = data.parent.find_all_next('table')[0]
    d = {}
    for tr in table.findAll("tr"):
        key = tr.find("th").text.strip(' \r\n\t').lower()
        value = tr.find("td").text.strip(' \r\n\t').lower()
        if key.find('.') < 0:
            d[key] = value
    d['price'] = get_price(file_path)
    return d

if __name__ == "__main__":
    matches = get_table_info('data/B00004SD9J')
    print matches