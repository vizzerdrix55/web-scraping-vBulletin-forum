#!/usr/bin/env python
# coding: utf-8

# Transforms all HTML-files in directory 'directory_in_str' to xml and takes caution to their filenames. date, title (where existing), username and content of a post will be extracted. Quotes will be exclude.
# Duration: 2 seconds per 100 HTML-Files (depending on your CPU)

import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import codecs
import logging

logging.basicConfig(filename='xml-transformation.log',
                    filemode='w',
                    format='%(asctime)s %(message)s',
                    level=logging.WARNING)
logging.critical('start')

directory_in_str = '' #put the path to your html-files here
directory = os.fsencode(directory_in_str)
filepaths =[]
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".html"): 
        filepaths.append(os.path.join(directory_in_str, filename))
    else:
        logging.error('skipped file that ends not with .html: %s' % file)

for file in filepaths:
    try:
        with codecs.open(file, 'r', 'utf-8') as f:
            page = f.read()
    except:
        logging.error('skipped %s because of UnicodeDecodeError' % file)
    else:
        soup = BeautifulSoup(page, 'lxml')
        postlist = soup.find_all('li', ['postbit'])
        if postlist:
            logging.info('HTML structure for postlist successfully checked')
        else:
            logging.error('other HTML structure than expected',
                          'for postlist')
        root = ET.Element('root')
        for post in postlist:
            post_node = ET.SubElement(root, 'post')
            date = post.find('div',['datetime'])
            if date:
                ET.SubElement(post_node, 'date').text = date.get_text()
            else:
                logging.error('no HTML structure found for date')
            title = post.find('div',['title'])
            if title:
                ET.SubElement(post_node, 'title').text = title.get_text()
            else:
                logging.error('no HTML structure found for title')
            username = post.find('span',['username'])
            if username:
                ET.SubElement(post_node, 'username').text                = username.get_text()
            else:
                logging.error('no HTML structure found for username')
            content = post.find('blockquote',['restore'])
            if content:
                bbcodes = content.find_all('div', ['bbcode_quote'])
                for bbcode in bbcodes: #exclude quotes
                    bbcode.decompose()
                ET.SubElement(post_node, 'content').text                = content.get_text()
            else:
                logging.error('no HTML structure found for content')
    tree = ET.ElementTree(root)
    tree.write('%s.xml' % file,)
    logging.critical('saved file %s.xml' % file)

logging.critical('end')