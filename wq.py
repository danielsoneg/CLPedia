#!/usr/bin/env python
# encoding: utf-8
import requests
import json
import sys
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

def getBody(title):
    html = requests.get('http://en.wikipedia.org/wiki/%s' % title)
    soup = BeautifulSoup(html.content)
    body = soup.find(id='mw-content-text')
    actualTitle = soup.find(id='firstHeading').text.strip()
    if body.find('p').text.strip().endswith('may refer to:'):
        return body.text # Is this a disambiguation page?
    for p in body.find_all('p'):
        if len(p.text.split(' ')) >= 10 and p.parent.name != 'td': # Kludge to try to get good info.
            para = p.text.strip()
            break
    return actualTitle, para

def run():
    sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
    sys.stderr = codecs.lookup('utf-8')[-1](sys.stderr)
    title = findTitle(search)
    actualTitle, para = getBody(title)
    print actualTitle, ' - https://en.wikipedia.org/wiki/%s' % title
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
    search = ' '.join(sys.argv[1:])
    run()