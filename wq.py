#!/usr/bin/env python
# encoding: utf-8
import requests
import json
import sys
import os
import codecs
from bs4 import BeautifulSoup

def apiRequest(query):
    if 'format' not in query: query['format']='json'
    resultjson = requests.get('http://en.wikipedia.org/w/api.php',params=query)
    result = json.loads(resultjson.content)
    return result

def findTitle(search):
    query = {'action':'opensearch','suggest':'True'}
    query['search'] = search
    search = apiRequest(query)
    title = search[1][0] if len(search[1]) != 0 else looseFind(search)
    return title

def looseFind(search):
    query = {'action':'query','list':'search','format':'json'}
    query['srsearch'] = search
    loose = apiRequest(query)
    return loose['query']['searchinfo']['suggestion']

def get_body(title, full_text):
    html = requests.get('http://en.wikipedia.org/wiki/%s' % title)
    soup = BeautifulSoup(html.content)
    body = soup.find(id='mw-content-text')
    actualTitle = soup.find(id='firstHeading').text.strip()
    para = None
    if full_text or body.find('p').text.strip().endswith('may refer to:'):
        return actualTitle, body.text
    for p in body.find_all('p'):
        if len(p.text.split(' ')) >= 10 and p.parent.name != 'td': # Kludge to try to get good info.
            para = p.text.strip()
            break
    if para == None:
        return actualTitle, body.text# hell with it, return Something.
    return actualTitle, para

def run(open_url=False, full_text=False):
    sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
    sys.stderr = codecs.lookup('utf-8')[-1](sys.stderr)
    title = findTitle(search)
    actualTitle, para = get_body(title, full_text)
    url = 'https://en.wikipedia.org/wiki/%s' % actualTitle
    if open_url:
        os.system('open "%s"' % url)
        sys.exit()
    print actualTitle, ' - ', url
    try:
        print para
    except UnicodeEncodeError:
        print para.encode('ascii','replace')

def usage():
    print """wq - Command Line Wiki Query-er
    Usage: wq <search term>"""

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    open_url = (sys.argv[1] == '--open')
    full_text = (sys.argv[1] == '--full')
    search = ' '.join(sys.argv[1:]) if not (open_url or full_text) else ' '.join(sys.argv[2:])
    run(open_url, full_text)