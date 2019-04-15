#!/usr/bin/env python
# coding: utf-8

# Generates URLs of every site of every forum and subforum of forum.pcgames.de and saves the list of URLs in threadurls_new


import requests
from bs4 import BeautifulSoup
import re
import random
import datetime
import logging
import sys
import time
logging.basicConfig(filename='log.log',
                    filemode='w',
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)

logging.info('start')

delays = [0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,
          0.93,0.94,0.95,0.96,0.97,0.98,0.99,1,1.01,1.02,1.03,1.04,1.05,
          1.06,1.07,1.08,1.09,1.1,1.11,1.12,1.13,1.14,1.15,1.16,1.17,1.18,
          1.19,1.2]

url = 'http://forum.pcgames.de/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


# URLs of forums
h2_forumtitles = soup.find_all('h2', ['forumtitle'])
forumtitles = []

if h2_forumtitles:
    for item in h2_forumtitles:
        a_forumtitle = item.find('a')
        if a_forumtitle:
            forumtitles.append(a_forumtitle.get('href'))
else:
    logging.error('other HTML structure than expected for URLs',
                  ' in h2_forumtitles')

print(forumtitles, file=open('forumtitles.txt', 'w'))
logging.info('printed %s items to list forumtitles' % len(forumtitles))


# URLs of subforums
li_subforum = soup.find_all('li', ['subforum'])
subforumtitles = []

if li_subforum:
    for item in li_subforum:
        a_subforumtitle = item.find('a')
        if a_subforumtitle:
            subforumtitles.append(a_subforumtitle.get('href'))
else:
    logging.error('other HTML structure than expected for URLs',
                  'in li_subforum')
    
print(subforumtitles, file=open('subforumtitles.txt', 'w'))
logging.info('printed %s items to list subforumtitles'              % len(subforumtitles))


#check structure for multiple pages
url='http://forum.pcgames.de/forum/9377509-frage-wo-',
'kann-ich-meinen-account-loeschen.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
x = soup.find('form', ['pagination'])

if x:
    logging.info('HTML structure for multiple pages follows expectation')
else:
    logging.error('unexpected HTML structure for multiple pages detected')


# URLs of forums incl. all sites
forumtitles_new = []


for item in forumtitles:
    delay = random.choice(delays) #randomly pick one delay
    time.sleep(delay)
    try:
        page = requests.get(item)
    except:
        e = sys.exc_info()[0]
        logging.error('ERROR: skipped %s because of %s' % (url, e))
    else:
        soup = BeautifulSoup(page.text, 'html.parser')
        x = soup.find('form', ['pagination'])
        if x is not None:
            pattern = re.compile(r'Seite\s\d+\svon\s(\d+)', re.I)
            pages = soup.find('a', text=pattern).text.strip()
            pages = int(pattern.match(pages).group(1))
            page_urls = ['{}/index{}.html'.format(item, p)
                         for p in range(1, pages + 1)]
            forumtitles_new.extend(page_urls)
        else:
            forumtitles_new.append(item)  

print(forumtitles_new, file=open('forumtitles_new.txt', 'w'))
logging.info('printed %s items to list forumtitles_new'              % len(forumtitles_new))


# URLs of subforums incl. all sites
subforumtitles_new = []

for item in subforumtitles:
    delay = random.choice(delays)
    time.sleep(delay)
    try:
        page = requests.get(item)
    except:
        e = sys.exc_info()[0]
        logging.error('ERROR: skipped %s because of %s' % (url, e))
    else:
        soup = BeautifulSoup(page.text, 'html.parser')
        x = soup.find('form', ['pagination'])
        if x is not None:
            pattern = re.compile(r'Seite\s\d+\svon\s(\d+)', re.I)
            pages = soup.find('a', text=pattern).text.strip()
            pages = int(pattern.match(pages).group(1))
            page_urls = ['{}/index{}.html'.format(item, p)
                         for p in range(1, pages + 1)]
            subforumtitles_new.extend(page_urls)
        else:
            subforumtitles_new.append(item)

print(subforumtitles_new, file=open('subforumtitles_new.txt', 'w'))
logging.info('printed %s items to list subforumtitles_new'              % len(subforumtitles_new))


# merge both lists
all_forumtitles_new = subforumtitles_new + forumtitles_new

print(all_forumtitles_new, file=open('all_forumtitles_new.txt', 'w'))


# URLs of threads (approximatel 14.18 seconds per 10 items)
threadurls = []

for item in all_forumtitles_new:
    delay = random.choice(delays)
    time.sleep(delay)
    try:
        page = requests.get(item)
    except:
        e = sys.exc_info()[0]
        logging.error('ERROR: skipped %s because of %s' % (url, e))
    else:
        soup = BeautifulSoup(page.text, 'html.parser')
        threadlist = soup.find_all('h3', ['threadtitle'])
        for item in threadlist:
            a_threads = item.find('a')
            if a_threads:
                threadurls.append(a_threads.get('href'))

print(threadurls, file=open('threadurls.txt', 'w'))
logging.info('printed %s items to list threadurls' % len(threadurls))


# URLs of threads incl. all site (aproximately 15.65 seconds per 10 items)
threadurls_new = []

for item in threadurls:
    delay = random.choice(delays)
    time.sleep(delay)
    try:
        page = requests.get(item)
    except:
        e = sys.exc_info()[0]
        logging.error('ERROR: skipped %s because of %s' % (url, e))
    else:
        soup = BeautifulSoup(page.text, 'html.parser')
        x = soup.find('form', ['pagination'])
        if x is not None:
            pattern = re.compile(r'Seite\s\d+\svon\s(\d+)', re.I)
            pages = soup.find('a', text=pattern).text.strip()
            pages = int(pattern.match(pages).group(1))
            page_urls = ['{}-{}.html'.format(item[:-5], p)
                         for p in range(1, pages + 1)]
            threadurls_new.extend(page_urls)
        else:
            threadurls_new.append(item)

print(threadurls_new, file=open('threadurls_new_.txt', 'w'))
logging.info('printed %s items to list threadurls_new'             % len(threadurls_new))
logging.info('end')