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

def get_table_info(file_path):
    soup = make_soup(file_path)
    table = soup.findAll('div')
    print table

    # The first tr contains the field names.
    # headings = [th.get_text() for th in table.find("tr").find_all("th")]

    # datasets = []
    # for row in table.find_all("tr")[1:]:
    #     dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
    #     datasets.append(dataset)


if __name__ == "__main__":
    matches = get_table_info('data/B000I97H68')
    print matches