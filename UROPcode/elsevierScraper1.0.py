#pip install pyOpenSSL
import requests
import json
from bs4 import BeautifulSoup as bs
import ssl
import time

'''
The elsevier search is kind of a tree structure:
"keyword --> a list of journals (a journal contain many articles) --> lists of articles
'''


journals = []
articles = []
abstracts = {}


def getJournals(url):
    global journals
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    html = requests.get(url,verify = False)
    data = json.loads(html.content)# response is in json format so we load it into a dictionary
    hits = data['hits']['hits']# target urls are hidden deep inside nested dictionaries and lists
    for hit in hits:
        journals.append(str(hit['_source']['url']+'/most-downloaded-articles'))

    return None

def getArtciels(url):
    global artciles
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    html = requests.get(url,verify = False)
    bsObj = bs(html.content, features='html.parser')
    
    for link in bsObj.findAll('a'):
        if 'href' in link.attrs:
            rawlink = link.attrs['href']
            if rawlink.startswith('https://www.sciencedirect.com/science/article/pii/'):
                articles.append(rawlink)
    
    return None

def getAbstracts(url):
    global abstracts
    
    # https://www.sciencedirect.com/science/article/pii/S0043135419301794
    # https://api.elsevier.com/content/article/pii/S0043135419301794
    # ?APIKey=ca5ec889b2aa7089a5e27c277cea8e90
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = requests.get(url,verify = False)
    bsObj = bs(html.content, features='lxml')
    
    title = bsObj.find('dc:title').text
    abstract = bsObj.find('dc:description').text
    abstract = abstract.replace('Abstract', ' ').strip()

    abstracts[title] = abstract
    
    return None


start = time.time()



# Search a key word
address = input("Please type in your keyword: ")
# https://site-search-api.prod.ecommerce.elsevier.com/search?
# query=catalyst%20for%20water%20splitting&labels=journals&start=0&limit=10&lang=en-xs
address = address.replace(' ', '%20')
address = 'https://site-search-api.prod.ecommerce.elsevier.com/search?query=' + address + '&labels=journals&start=0&limit=100&lang=en-xs'
######################################################################################
####### increase the number following "&limit=" to increase the number of URLs #######
######################################################################################

getJournals(address)

for url in journals:
    getArtciels(url)

for article in articles:
    link = 'https://api.elsevier.com/content/article/pii/' + article[-17::] + '?APIKey=ca5ec889b2aa7089a5e27c277cea8e90'
    getAbstracts(link)

with open('test3.txt', 'w') as file:
     file.write(json.dumps(abstracts)) # use `json.loads` to do the reverse
     
end = time.time()

#print(abstracts)
print(end-start)

'''
Take note that there are duplicated articles (465 duplicates for 21810 articles) 
based on the length comparison. 
'''

'''
Test 1
It takes 372.5433921813965 seconds to extract 103 paper abstracts with corresponding titles
from 5 journals and store the abstracts as values and their titles as keys into a dictionary.
'''

'''
Test 2
It takes 741.9820911884308 seconds to extract 215 paper abstracts with corresponding titles
from 10 journals and store the abstracts as values and their titles as keys into a dictionary.
'''