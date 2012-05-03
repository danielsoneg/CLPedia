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
    firstPara = body.find('p').text.strip()
    if firstPara.endswith('may refer to:'): 
        return body.text
    return actualTitle, firstPara

def run():
    sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
    sys.stderr = codecs.lookup('utf-8')[-1](sys.stderr)
    title = findTitle(search)
    actualTitle, firstPara = getBody(title)
    print actualTitle, ' - https://en.wikipedia.org/wiki/%s' % title
    try:
        print firstPara
    except UnicodeEncodeError:
        print firstPara.encode('ascii','replace')

def usage():
    print """wq - Command Line Wiki Query-er
    Usage: wq <search term>"""

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    search = ' '.join(sys.argv[1:])
    run()