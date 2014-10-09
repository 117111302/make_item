#! /usr/bin/env python
# -*- coding: utf8 -*-

import re
import os
import sys
import csv
import codecs
import shutil

FIELDNAMES = ['item_no', 'title', 'price']
DELIMITER = ','
QUOTE_CHARACTER = '"'
SCOPE = 15
PREFIX = '116'
BASE = os.path.realpath(os.path.dirname(__file__))


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
        item_no, price = re.sub('JTYL', '', row['outer_id']).strip().split(' ')
        price = int(price.split('P')[1]) + SCOPE
        item_no = '%s%s' % (PREFIX, item_no)
        pictures = [(lambda x: x.split(':')[0])(x) for x in row['picture'].split(';')]
        item = dict(title=title, price=price, item_no=item_no, pictures=pictures)
        items.append(item)
    return items


def mkdir(name):
    """create directroy to save item file
    """
    ipath = os.path.join(BASE, name)
#    if os.path.isdir(ipath):
#	print '%s is existed!' % (ipath,)
#	os.rmdir(ipath)
    if not os.path.exists(ipath):
        os.mkdir(ipath)
    return ipath


def copy_to_path(target, dest):
    """copy obj to destination directroy
    """
    shutil.copyfile(target, dest)


def main():
    csvfile = sys.argv[1]
    pic_path = sys.argv[2]
    with open(csvfile, 'rb') as f:
        next(f)
        items = parse_items(csv.DictReader(f))
    # write items to file
    with open('file.csv', 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        for item in items:
            ipath = mkdir(item['item_no'])
	    print 'Create path:', ipath
            for pic in item['pictures']:
		if not pic: continue
                f_path = os.path.join(BASE, pic_path, '%s.tbi' % (pic,))
		t_path = os.path.join(ipath, '%s.jpg' % (pic,))
                copy_to_path(f_path, t_path)
	    item.pop('pictures')
	    writer.writerow(item)
#	    f.write(str(item)+'\n')
    print 'Make items total: %d' % len(items)


if __name__ == '__main__':
    main()
