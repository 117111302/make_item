#! /usr/bin/env python
# -*- coding: utf8 -*-

import re
import os
import sys
import csv
import codecs
import shutil
from subprocess import check_call, CalledProcessError

FIELDNAMES = ['item_no', 'title', 'price']
DELIMITER = ','
QUOTE_CHARACTER = '"'
PREFIX = '116'
BASE = os.path.realpath(os.path.dirname(__file__))
PIFAJIA = '\xe6\x89\xb9\xe5\x8f\x91\xe4\xbb\xb7%s'
JTYL = '\xe9\x94\xa6\xe8\x97\xa4\xe4\xbe\x9d\xe6\x81\x8b'
SCOPE = int(sys.argv[3])


def unicode_csv_reader(unicode_csv_data, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.DictReader(unicode_csv_data,
                            **kwargs)
    for row in csv_reader:
        yield row


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def get_main_pic(desc_str, t_path):
    """download pic to path
    """
    urls = get_pic_url_from_desc(desc_str)
    print urls
    for url in urls:
        download(url, t_path)


def get_pic_url_from_desc(desc_str):
    return re.findall(r'(https?://\S+jpg)', desc_str)


def download(href, localpath, verbosity=1):
    "Download this to local path"
    vopt = {0: '-q', 1: '-nv', 2: '-v'}.get(verbosity, 1)
    cmd = ['wget', vopt, '-P', localpath, '--no-check-certificate']
    cmd.append(href)
    try:
        return check_call(cmd)
    except CalledProcessError as err:
        raise


def parse_items(csv_reader):
    """parse items from csv file
    """
    items = []
    for row in csv_reader:
#        title =  re.sub('\w+', '', row['title'].decode('gbk').encode('utf-8').replace(JTYL, ''))
#        item_no, price = re.sub('JTYL', '', row['outer_id']).strip().split(' ')
#        price = PIFAJIA % str(int(price.split('P')[1]) + SCOPE)
        title = row['title'].decode('gbk').encode('utf-8')
        item_no, price = row['outer_id'].strip().split('P')
        price = PIFAJIA % str(int(price) + SCOPE)

        item_no = '%s%s' % (PREFIX, item_no)
        pictures = [(lambda x: x.split(':')[0])(x) for x in row['picture'].split(';')]
        description = row['description']
        item = dict(title=title, price=price, item_no=item_no, pictures=pictures, description=description)
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
    """
    change the item name to what you want in csvfile
    run it as ./make_pictures.py csvfile tbifilepath your_scope_price
    """
    csvfile = sys.argv[1]
    pic_path = sys.argv[2]
    with open(csvfile, 'rb') as f:
        next(f)
        items = parse_items(csv.DictReader(f))
    # write items to file
    for item in items:
        ipath = mkdir(item['item_no'])
        print 'Create path:', ipath
        get_main_pic(item['description'], ipath)
        for pic in item['pictures']:
            if not pic: continue
            f_path = os.path.join(BASE, pic_path, '%s.tbi' % (pic,))
	    t_path = os.path.join(ipath, '%s.jpg' % (pic,))
            copy_to_path(f_path, t_path)
        with open(os.path.join(ipath, 'jiage.txt'), 'wb') as f:
            #writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
	    item.pop('pictures')
            item.pop('description')
	    f.write(','.join(item.values()))
	    #writer.writerow(item)
#	    f.write(str(item)+'\n')
    print 'Make items total: %d' % len(items)


if __name__ == '__main__':
    main()
