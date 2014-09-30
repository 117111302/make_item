#! /usr/bin/env python
# -*- coding: utf8 -*-

import re
import sys
import csv
import codecs

FIELD_NAMES = ['title', 'inputValues', 'picture' , 'outer_id']
DELIMITER = ','
QUOTE_CHARACTER = '"'
SCOPE = 15
PREFIX = '116'


def unicode_csv_reader(unicode_csv_data, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.DictReader(unicode_csv_data,
                            **kwargs)
    for row in csv_reader:
        yield row

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def parse_items(csv_reader):
    """parse items from csv file
    """
    items = []
    for row in csv_reader:
        title =  row['title']
        item_no, price = re.sub('JTYL', '', row['outer_id']).split(' ')
        price = int(price.split('P')[1]) + SCOPE
        item_no = '%s%s' % (PREFIX, item_no)
        pictures = [(lambda x: x.split(':')[0])(x) for x in row['picture'].split(';')]
        item = dict(title=title, price=price, item_no=item_no, pictures=pictures)
        items.append(item)
    return items


def mkdir(name):
    """create directroy to save item file
    """
    pass


def change_ext():
    """change file extension
    """
    pass


def copy_to_path(obj, dest)
    """copy obj to destination directroy
    """
    pass


def main():
    csvfile = sys.argv[1]
#    with codecs.open(csvfile, 'rU', 'utf-16') as f:
    with open(csvfile, 'rb') as f:
        next(f)
        items = parse_items(unicode_csv_reader(f))
    print items
    print '*'*80
    # write items to file
    with open('file.txt', 'rw') as f:
        for item in items:
            ipath = mkdir(item[item_no])
            for pic in pictures:
                name = change_ext(pic)
                copy_to_path(name, ipath)
        f.write(item)


if __name__ == '__main__':
    main()
